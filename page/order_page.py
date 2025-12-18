import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class OrderPage(BasePage):
    # ===== форма "для кого самокат" =====
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")

    # Метро (react select-search)
    METRO_INPUT = (By.CSS_SELECTOR, "input.select-search__input")
    METRO_ANY_OPTION = (By.CSS_SELECTOR, ".select-search__select .select-search__row")  # любой пункт

    PHONE_INPUT = (By.XPATH, "//input[contains(@placeholder,'Телефон')]")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # ===== форма "про аренду" =====
    DELIVERY_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")

    # ВАЖНО: кликаем не placeholder, а контрол
    RENT_DROPDOWN = (By.CLASS_NAME, "Dropdown-control")
    RENT_OPTION_BY_TEXT = (By.XPATH, "//div[contains(@class,'Dropdown-option') and normalize-space(text())='{text}']")

    COLOUR_BLACK = (By.ID, "black")
    COLOUR_GREY = (By.ID, "grey")

    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")

    ORDER_BUTTON = (By.XPATH, "//div[contains(@class,'Order_Buttons')]//button[text()='Заказать']")
    YES_BUTTON = (By.XPATH, "//button[text()='Да']")

    SUCCESS_MODAL = (By.XPATH, "//div[contains(@class,'Order_ModalHeader') and contains(.,'Заказ оформлен')]")

    # Datepicker overlay
    DATEPICKER = (By.CLASS_NAME, "react-datepicker")

    # ---------- helpers ----------
    def _rent_option(self, text: str):
        return (self.RENT_OPTION_BY_TEXT[0], self.RENT_OPTION_BY_TEXT[1].format(text=text))

    def _wait_invisible(self, locator, timeout: int = 5) -> bool:
        """Локальный wait на исчезновение (чтобы не править BasePage)."""
        try:
            self._wait(timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def _close_datepicker(self):
        """Закрыть календарь и дождаться, что он исчез (иначе будет click intercepted)."""
        # ESC обычно закрывает, но иногда нужно "кликнуть мимо"
        try:
            inp = self.wait_for_visible(self.DELIVERY_INPUT, timeout=5)
            inp.send_keys(Keys.ESCAPE)
        except Exception:
            pass

        if not self._wait_invisible(self.DATEPICKER, timeout=5):
            # добиваем "кликом по body" (через BasePage.execute_script, если у тебя он есть)
            try:
                self.execute_script("document.body.click();")
            except Exception:
                # если execute_script нет — просто табом уводим фокус
                try:
                    inp = self.wait_for_visible(self.DELIVERY_INPUT, timeout=3)
                    inp.send_keys(Keys.TAB)
                except Exception:
                    pass
            # ещё раз ждём исчезновение
            self._wait_invisible(self.DATEPICKER, timeout=5)

    # ---------- steps ----------
    @allure.step("Заполняем форму 'для кого самокат'")
    def fill_customer_form(self, first_name, last_name, address, metro, phone):
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.ADDRESS_INPUT, address)

        # выбор станции метро: ждём появление списка, затем ARROW_DOWN + ENTER
        metro_input = self.wait_for_visible(self.METRO_INPUT)
        metro_input.click()
        metro_input.send_keys(metro)

        # дождаться, что варианты появились (иначе ARROW_DOWN уйдёт в никуда)
        self.wait_for_all_present(self.METRO_ANY_OPTION, timeout=10)

        metro_input.send_keys(Keys.ARROW_DOWN)
        metro_input.send_keys(Keys.ENTER)

        self.send_keys(self.PHONE_INPUT, phone)
        self.click(self.NEXT_BUTTON)

    @allure.step("Заполняем форму 'про аренду'")
    def fill_rent_form(self, **data):
        # поддержим разные названия ключей
        date = data.get("date") or data.get("delivery_date") or data.get("deliveryDate")
        comment = data.get("comment", "")
        rent_text = data.get("rent_period") or data.get("period") or data.get("rentText") or "сутки"

        # цвет: можно передать locator или строку "black"/"grey"
        colour_locator = data.get("colour_locator") or data.get("color_locator") or data.get("colour")
        color = data.get("color") or data.get("colour")

        # 1) дата
        date_input = self.wait_for_visible(self.DELIVERY_INPUT, timeout=10)
        date_input.click()
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.ENTER)   # иногда выбирает дату
        date_input.send_keys(Keys.ESCAPE)  # закрывает календарь

        self._close_datepicker()  # ключевой фикс от click intercepted

        # 2) срок аренды
        dropdown = self.wait_for_clickable(self.RENT_DROPDOWN, timeout=10)
        self.scroll_into_view_center(dropdown)
        dropdown.click()
        self.click(self._rent_option(rent_text), timeout=10)

        # 3) цвет (если передали)
        if colour_locator:
            # если строка "black"/"grey"
            if isinstance(colour_locator, str):
                if colour_locator.lower() == "black":
                    self.click(self.COLOUR_BLACK)
                elif colour_locator.lower() == "grey":
                    self.click(self.COLOUR_GREY)
            else:
                self.click(colour_locator)
        elif isinstance(color, str):
            if color.lower() == "black":
                self.click(self.COLOUR_BLACK)
            elif color.lower() == "grey":
                self.click(self.COLOUR_GREY)

        # 4) комментарий
        if comment:
            self.send_keys(self.COMMENT_INPUT, comment)

        # 5) оформить + подтвердить
        self.click(self.ORDER_BUTTON, timeout=10)
        self.click(self.YES_BUTTON, timeout=10)

    @allure.step("Проверяем, что заказ успешно оформлен")
    def is_order_successful(self, timeout: int = 10) -> bool:
        try:
            self.wait_for_visible(self.SUCCESS_MODAL, timeout=timeout)
            return True
        except TimeoutException:
            return False

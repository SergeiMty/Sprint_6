from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    URL = "https://qa-scooter.praktikum-services.ru/"

    # 🔹 кнопка куки
    COOKIE_ACCEPT_BUTTON = (By.ID, "rcc-confirm-button")

    # 🔹 ОБЩИЙ локатор для обеих кнопок "Заказать"
    ORDER_BUTTONS = (By.XPATH, "//button[text()='Заказать']")

    # ======= КУКИ =======
    def accept_cookies(self):
        """Закрываем баннер с куками, если он есть."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.COOKIE_ACCEPT_BUTTON)
            ).click()
        except Exception:
            # если баннера нет — просто идём дальше
            pass

    # ======= КНОПКИ "ЗАКАЗАТЬ" =======
    def click_order_button_top(self):
        """Кликаем по верхней кнопке 'Заказать'."""
        buttons = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTONS)
        )
        # buttons — это уже список элементов
        buttons[0].click()

    def click_order_button_bottom(self):
        """Кликаем по нижней кнопке 'Заказать' (если понадобится второй тест)."""
        buttons = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located(self.ORDER_BUTTONS)
        )
        if len(buttons) < 2:
            raise AssertionError("Нижняя кнопка 'Заказать' не найдена на странице")
        buttons[1].click()

    # ======= FAQ =======
    def faq_question_locator(self, index: int):
        return By.ID, f"accordion__heading-{index}"

    def faq_answer_locator(self, index: int):
        return By.ID, f"accordion__panel-{index}"

    def click_faq_question(self, index: int):
        locator = self.faq_question_locator(index)

        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        self.driver.execute_script("window.scrollBy(0, -100);")

        element.click()

    def get_faq_answer_text(self, index: int) -> str:
        locator = self.faq_answer_locator(index)
        element = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text


import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class MainPage(BasePage):
    URL = "https://qa-scooter.praktikum-services.ru/"

    # 🔹 кнопка куки
    COOKIE_ACCEPT_BUTTON = (By.ID, "rcc-confirm-button")

    # 🔹 ОБЩИЙ локатор для обеих кнопок "Заказать"
    ORDER_BUTTONS = (By.XPATH, "//button[text()='Заказать']")

    # ======= НАВИГАЦИЯ =======
    @allure.step("Открываем главную страницу самоката")
    def open_main_page(self):
        self.open(self.URL)

    # ======= КУКИ =======
    @allure.step("Закрываем баннер с куками, если он есть")
    def accept_cookies(self):
        try:
            self.click(self.COOKIE_ACCEPT_BUTTON, timeout=5)
        except TimeoutException:
            # если баннера нет — просто идём дальше
            pass

    # ======= КНОПКИ 'ЗАКАЗАТЬ' =======
    @allure.step("Кликаем по верхней кнопке 'Заказать'")
    def click_order_button_top(self):
        buttons = self.wait_for_all_present(self.ORDER_BUTTONS, timeout=5)
        buttons[0].click()

    @allure.step("Кликаем по нижней кнопке 'Заказать'")
    def click_order_button_bottom(self):
        buttons = self.wait_for_all_present(self.ORDER_BUTTONS, timeout=5)
        if len(buttons) < 2:
            raise AssertionError("Нижняя кнопка 'Заказать' не найдена на странице")
        buttons[1].click()

    # ======= FAQ =======
    @allure.step("Получаем локатор вопроса FAQ с индексом {index}")
    def faq_question_locator(self, index: int):
        return By.ID, f"accordion__heading-{index}"

    @allure.step("Получаем локатор ответа FAQ с индексом {index}")
    def faq_answer_locator(self, index: int):
        return By.ID, f"accordion__panel-{index}"

    @allure.step("Кликаем по вопросу FAQ с индексом {index}")
    def click_faq_question(self, index: int):
        locator = self.faq_question_locator(index)

        element = self.wait_for_clickable(locator, timeout=5)

        # вместо прямого self.driver.execute_script — методы из BasePage
        self.scroll_into_view_center(element)
        self.scroll_by(0, -100)

        element.click()

    @allure.step("Получаем текст ответа FAQ с индексом {index}")
    def get_faq_answer_text(self, index: int) -> str:
        locator = self.faq_answer_locator(index)
        return self.get_text(locator, timeout=5)




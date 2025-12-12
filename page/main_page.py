# page/main_page.py
import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class MainPage(BasePage):
    URL = "https://qa-scooter.praktikum-services.ru/"

    # Кнопки "Заказать"
    ORDER_BUTTON_TOP = (By.XPATH, "(//button[text()='Заказать'])[1]")
    ORDER_BUTTON_MIDDLE = (By.XPATH, "(//button[text()='Заказать'])[2]")

    # Куки
    COOKIE_ACCEPT_BUTTON = (By.ID, "rcc-confirm-button")

    # FAQ
    FAQ_QUESTION_LOCATOR = (By.ID, "accordion__heading-{index}")
    FAQ_ANSWER_LOCATOR = (By.ID, "accordion__panel-{index}")

    # Логотипы
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")

    @allure.step("Открываем главную страницу")
    def open_main_page(self):
        self.open(self.URL)

    @allure.step("Закрываем баннер с куками, если он есть")
    def accept_cookies(self):
        try:
            self.click(self.COOKIE_ACCEPT_BUTTON, timeout=5)
        except TimeoutException:
            pass

    @allure.step("Нажимаем верхнюю кнопку 'Заказать'")
    def click_order_button_top(self):
        self.click(self.ORDER_BUTTON_TOP)

    @allure.step("Нажимаем кнопку 'Заказать' в середине страницы")
    def click_order_button_middle(self):
        self.click(self.ORDER_BUTTON_MIDDLE)

    @allure.step("Переходим по лого 'Самокат'")
    def click_scooter_logo(self):
        self.click(self.SCOOTER_LOGO)

    @allure.step("Переходим по лого 'Яндекс'")
    def click_yandex_logo(self):
        self.click(self.YANDEX_LOGO)

    # ====== РАБОТА С FAQ ======

    @allure.step("Кликаем по вопросу FAQ с индексом {index}")
    def click_faq_question(self, index: int):
        # собираем реальный локатор вида (By.ID, "accordion__heading-0")
        locator = (
            self.FAQ_QUESTION_LOCATOR[0],
            self.FAQ_QUESTION_LOCATOR[1].format(index=index),
        )
        question = self.wait_for_visible(locator)
        self.scroll_into_view_center(question)
        question.click()

    @allure.step("Получаем текст ответа FAQ для вопроса с индексом {index}")
    def get_faq_answer_text(self, index: int) -> str:
        locator = (
            self.FAQ_ANSWER_LOCATOR[0],
            self.FAQ_ANSWER_LOCATOR[1].format(index=index),
        )
        answer = self.wait_for_visible(locator)
        self.scroll_into_view_center(answer)
        return answer.text

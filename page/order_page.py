import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base_page import BasePage


class OrderPage(BasePage):
    # ===== форма "для кого самокат" =====
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.CSS_SELECTOR, "input.select-search__input")
    PHONE_INPUT = (By.XPATH, "//input[contains(@placeholder,'Телефон')]")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # ===== форма "про аренду" =====
    DELIVERY_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    TIME_OF_RENT = (By.CLASS_NAME, "Dropdown-placeholder")
    RENT_FOR_DAY = (
        By.XPATH,
        "//div[contains(@class,'Dropdown-option') and text()='сутки']",
    )
    COLOUR_BLACK = (By.ID, "black")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Заказать']")
    YES_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MODAL = (By.XPATH, "//*[contains(text(),'Заказ оформлен')]")

    @allure.step("Заполняем форму 'для кого самокат'")
    def fill_customer_form(self, first_name, last_name, address, metro, phone):
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(selfLAST_NAME_INPUT, last_name)
        self.send_keys(self.ADDRESS_INPUT, address)

        # выбор станции метро
        metro_input = self.is_visible(self.METRO_INPUT)
        metro_input.click()
        metro_input.send_keys(metro)
        metro_input.send_keys(Keys.ARROW_DOWN)
        metro_input.send_keys(Keys.ENTER)

        self.send_keys(self.PHONE_INPUT, phone)
        self.click(self.NEXT_BUTTON)

    @allure.step("Заполняем форму 'про аренду'")
    def fill_rent_form(self, date, comment, colour_locator):
        self.send_keys(self.DELIVERY_INPUT, date)
        self.click(self.TIME_OF_RENT)
        self.click(self.RENT_FOR_DAY)
        self.click(colour_locator)
        self.send_keys(self.COMMENT_INPUT, comment)
        self.click(self.ORDER_BUTTON)
        self.click(self.YES_BUTTON)

    @allure.step("Проверяем, что заказ успешно оформлен")
    def is_order_successful(self, timeout: int = 10) -> bool:
        modal = self.is_visible(self.SUCCESS_MODAL, timeout=timeout)
        return modal is not None

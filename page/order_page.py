import allure
from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderPage(BasePage):
    # Форма "для кого самокат"
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    PHONE_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Телефон')]")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # Форма "про аренду"
    DELIVERY_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    TIME_OF_RENT = (By.CLASS_NAME, "Dropdown-placeholder")
    RENT_FOR_DAY = (
        By.XPATH,
        "//div[contains(@class,'Dropdown-option') and text()='сутки']",
    )
    COLOUR_BLACK = (By.ID, "black")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")

    ORDER_BUTTON = (By.XPATH, "(//button[text()='Заказать'])[last()]")
    YES_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MODAL = (By.XPATH, "//*[contains(text(),'Заказ оформлен')]")

    # Заполнение формы "для кого самокат"
    @allure.step("Заполняем форму заказа самоката")
    def fill_customer_form(self, first_name, last_name, address, metro, phone):
        wait = WebDriverWait(self.driver, 5)
        
        wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT)).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(address)

        # вводим метро и выбираем первый вариант из списка
        metro_input = self.driver.find_element(*self.METRO_INPUT)
        metro_input.send_keys(metro)
        metro_input.send_keys(Keys.DOWN)
        metro_input.send_keys(Keys.ENTER)

        # ждем пока появится телефон (без данного )
        wait.until(EC.visibility_of_element_located(self.PHONE_INPUT)).send_keys(phone)

        self.click(self.NEXT_BUTTON)

    # Заполнение формы "про аренду"
    def fill_rent_form(self, date, comment, colour_locator):
        wait = WebDriverWait(self.driver, 5)
        date_input = wait.until(
            EC.element_to_be_clickable(self.DELIVERY_INPUT)
        )
        date_input.click()
        date_input.clear()
        date_input.send_keys(date)

        date_input.send_keys(Keys.ENTER)

        # срок аренды – открываем дропдаун и выбираем «сутки»
        dropdown = wait.until(
            EC.element_to_be_clickable(self.TIME_OF_RENT)
        )
        dropdown.click()

        rent_for_day = wait.until(
            EC.element_to_be_clickable(self.RENT_FOR_DAY)
        )
        rent_for_day.click()
        

        # цвет (черный / серый – передаём локатором)
        wait.until(
            EC.element_to_be_clickable(colour_locator)
        ).click()

        # комментарий
        self.driver.find_element(*self.COMMENT_INPUT).send_keys(comment)

        # оформить заказ
        self.click(self.ORDER_BUTTON)

        try:
            self.click(self.YES_BUTTON)
        except TimeoutException:
            pass

    # Проверка результата
    def is_order_successful(self) -> bool:
        self.is_visible(self.SUCCESS_MODAL)
        return True

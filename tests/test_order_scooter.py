import allure

from page.main_page import MainPage
from page.order_page import OrderPage
from data import ORDER_CUSTOMER_DATA, ORDER_RENT_DATA


class TestOrderScooter:

    @allure.title("Заказ самоката через верхнюю кнопку 'Заказать'")
    def test_order_scooter_from_top_button(self, driver):
        main = MainPage(driver)
        main.open_main_page()
        main.accept_cookies()
        main.click_order_button_top()

        order = OrderPage(driver)
        order.fill_customer_form(**ORDER_CUSTOMER_DATA)
        order.fill_rent_form(**ORDER_RENT_DATA)

        assert order.is_order_successful()

    @allure.title("Заказ самоката через кнопку 'Заказать' в середине страницы")
    def test_order_scooter_from_middle_button(self, driver):
        main = MainPage(driver)
        main.open_main_page()
        main.accept_cookies()
        main.scroll_by(0, 600)  # чуть прокрутить до кнопки, при желании
        main.click_order_button_middle()

        order = OrderPage(driver)
        order.fill_customer_form(**ORDER_CUSTOMER_DATA)
        order.fill_rent_form(**ORDER_RENT_DATA)

        assert order.is_order_successful()

    @allure.title("Переход по лого 'Самокат' ведёт на главную страницу")
    def test_scooter_logo_link(self, driver):
        main = MainPage(driver)
        main.open_main_page()
        main.accept_cookies()

        main.click_scooter_logo()
        # если переход в этой же вкладке, просто ждём
        main.wait_for_url_contains("qa-scooter", timeout=5)

    @allure.title("Переход по лого 'Яндекс' ведёт на страницу Дзен")
    def test_yandex_logo_link(self, driver):
        main = MainPage(driver)
        main.open_main_page()
        main.accept_cookies()

        main.click_yandex_logo()
        # логотип открывает Дзен в новой вкладке
        driver.switch_to.window(driver.window_handles[-1])
        main.wait_for_url_contains("dzen.ru", timeout=10)

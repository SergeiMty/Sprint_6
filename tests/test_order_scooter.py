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
        main.scroll_by(0, 600)
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

        assert main.go_to_scooter_home_via_logo(), f"Не попали на главную Самоката. URL: {main.get_current_url()}"

    @allure.title("Переход по лого 'Яндекс' ведёт на страницу Дзен")
    def test_yandex_logo_link(self, driver):
        main = MainPage(driver)
        main.open_main_page()
        main.accept_cookies()

        assert main.open_dzen_from_yandex_logo(), f"Не попали на Dzen. URL: {main.get_current_url()}"

from page.main_page import MainPage
from page.order_page import OrderPage


def test_order_scooter_from_top_button(driver):
    main = MainPage(driver)
    main.open(MainPage.URL)
    main.accept_cookies()
    main.click_order_button_top()

    order = OrderPage(driver)
    order.fill_customer_form(
        first_name="Сергей",
        last_name="Сергеев",
        address="ул. Тестовая, д. 1",
        metro="Черкизовская",
        phone="+79055333030",
    )

    order.fill_rent_form(
        date="31.12.2025",
        comment="Тест",
        colour_locator=OrderPage.COLOUR_BLACK,
    )

    assert order.is_order_successful()


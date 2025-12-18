import pytest
import allure

from page.main_page import MainPage
from data import FAQ_CASES


class TestFAQQuestions:

    @allure.title("Проверка FAQ: {index}")
    @pytest.mark.parametrize("index, expected", FAQ_CASES)
    def test_faq_answer_text(self, driver, index, expected):
        main = MainPage(driver)
        main.open_main_page()
        main.accept_cookies()

        main.click_faq_question(index)
        actual = main.get_faq_answer_text(index)

        assert actual == expected, f"FAQ[{index}] ожидали: {expected!r}, получили: {actual!r}"






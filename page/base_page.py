from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # ====== Базовый WebDriverWait ======
    def _wait(self, timeout: int | None = None) -> WebDriverWait:
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time)

    # ====== ОЖИДАНИЯ ЭЛЕМЕНТОВ ======
    def wait_for_visible(self, locator, timeout: int | None = None):
        """Ждём, пока элемент станет видимым."""
        return self._wait(timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout: int | None = None):
        """Ждём, пока элемент станет кликабельным."""
        return self._wait(timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_all_present(self, locator, timeout: int | None = None):
        """Ждём, пока все элементы по локатору появятся в DOM."""
        return self._wait(timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    # ====== БАЗОВЫЕ ДЕЙСТВИЯ С ЭЛЕМЕНТАМИ ======
    def click(self, locator, timeout: int | None = None):
        """Клик по элементу с ожиданием кликабельности."""
        element = self.wait_for_clickable(locator, timeout)
        element.click()
        return element

    def get_text(self, locator, timeout: int | None = None) -> str:
        """Получаем текст элемента."""
        element = self.wait_for_visible(locator, timeout)
        return element.text

    def is_visible(self, locator, timeout: int | None = None):
        """Возвращает элемент, если он видим (или кидает TimeoutException)."""
        return self.wait_for_visible(locator, timeout)

    def send_keys(self, locator, text: str, timeout: int | None = None) -> None:
        """Вводим текст в поле."""
        elem = self.wait_for_visible(locator, timeout)
        elem.clear()
        elem.send_keys(text)

    # ====== НАВИГАЦИЯ ======
    def open(self, url: str) -> None:
        """Открываем URL."""
        self.driver.get(url)

    def wait_for_url_contains(self, text: str, timeout: int | None = None) -> None:
        """Ждём, пока URL будет содержать указанный текст."""
        self._wait(timeout).until(EC.url_contains(text))

    # ====== ОБЁРТКИ НАД driver.execute_script ======
    def execute_script(self, script: str, *args):
        """Единая точка для любых JS-скриптов."""
        return self.driver.execute_script(script, *args)

    def scroll_into_view_center(self, element):
        """Скроллим элемент в центр экрана."""
        self.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def scroll_by(self, x: int, y: int):
        """Просто скролл окна на заданное количество пикселей."""
        self.execute_script(
            "window.scrollBy(arguments[0], arguments[1]);", x, y
        )




import os
import sys
import ctypes
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from dotenv import load_dotenv
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


def is_admin() -> bool:
    """Проверяет, запущен ли скрипт с правами администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def require_admin() -> None:
    """Требует запуска с правами администратора."""
    if not is_admin():
        print("Ошибка: скрипт должен запускаться от имени администратора!")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    print("Скрипт запущен с правами администратора")


def check_path(path: str) -> None:
    """Проверяет существование указанных путей."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Путь не найден: {path}.")
    else:
        print(f'Путь {path} существует.')


def setup_chrome() -> webdriver.Chrome:
    """Настройка и возврат экземпляра WebDriver для Chrome."""
    chrome_options = webdriver.ChromeOptions()

    chrome_path = os.getenv("CHROME_PATH")
    if chrome_path:
        chrome_options.binary_location = chrome_path

    if os.getenv("HEADLESS_MODE", "true").lower() == "true":
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Драйвер Chrome успешно инициализирован")
    return driver


def setup_firefox() -> webdriver.Firefox:
    """Настройка и возврат экземпляра WebDriver для Firefox."""
    firefox_options = webdriver.FirefoxOptions()

    firefox_path = os.getenv("FIREFOX_PATH")
    if firefox_path:
        firefox_options.binary_location = firefox_path

    if os.getenv("HEADLESS_MODE", "true").lower() == "true":
        firefox_options.add_argument("--headless")

    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    print("Драйвер Firefox успешно инициализирован")
    return driver


def setup_driver() -> webdriver.Remote:
    """Настройка и возврат экземпляра WebDriver в зависимости от переменной окружения BROWSER."""
    browser = os.getenv("BROWSER")
    if browser == "Chrome":
        return setup_chrome()
    elif browser == "Firefox":
        return setup_firefox()
    else:
        raise EnvironmentError("Переменная окружения BROWSER не установлена, либо указана некорректно.")


def parse_products(driver: webdriver.Chrome | webdriver.Firefox, query: str) -> List[Dict[str, str]]:
    """Парсит товары с Wildberries."""
    driver.get(f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}")
    time.sleep(5)

    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    return [
        {
            "name": item.find_element(By.CSS_SELECTOR, ".product-card__name").text,
            "price": int(item.find_element(By.CSS_SELECTOR, ".price__lower-price").text
                         .replace("₽", "")
                         .replace(" ", "")),
            "url": item.find_element(By.CSS_SELECTOR, "a.product-card__link").get_attribute("href")
        }
        for item in driver.find_elements(By.CSS_SELECTOR, ".product-card")
        if item
    ]


def filter_products(products: List[Dict], min_price: int, max_price: int, keyword: str) -> List[Dict]:
    """Фильтрует товары по цене и наличию ключевого слова в названии."""
    keyword_lower = keyword.lower()
    return [
        product for product in products
        if (min_price <= product['price'] <= max_price) and (keyword_lower in product['name'].lower())
    ]


def parse_wildberries(query: str, min_price: int, max_price: int, keyword: str) -> List[Dict]:
    """Основная функция парсинга Wildberries."""
    require_admin()

    if os.getenv("BROWSER") == 'Firefox':
        path = os.getenv("FIREFOX_PATH")
    elif os.getenv("BROWSER") == 'Chrome':
        path = os.getenv("CHROME_PATH")
    else:
        path = None

    if not path:
        raise EnvironmentError("Необходимые переменные окружения не установлены")

    check_path(path)

    driver = setup_driver()
    try:
        products = parse_products(driver, query)
        filter_product = filter_products(products, min_price, max_price, keyword)
        return filter_product
    finally:
        driver.quit()


if __name__ == "__main__":

    try:
        results = parse_wildberries(
            query=os.getenv("PRODUCT"),
            min_price=int(os.getenv("MIN_PRICE")),
            max_price=int(os.getenv("MAX_PRICE")),
            keyword=os.getenv("KEYWORD")
        )
        print(f"Найдено товаров: {len(results)}")
    except Exception as e:
        print(f"Ошибка при выполнении: {e}")
        sys.exit(1)
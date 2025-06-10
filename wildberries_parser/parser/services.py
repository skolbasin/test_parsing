from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from parser.models import Product


def parse_wildberries(query, min_price, max_price, color):
    # Настраиваем Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Фоновый режим
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Открываем страницу поиска
    driver.get(f"https://www.wildberries.ru/catalog/0/search.aspx?search={query}")
    time.sleep(5)  # Ждем загрузки

    # Прокрутка для подгрузки всех товаров
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Парсим товары
    products = []
    items = driver.find_elements(By.CSS_SELECTOR, ".product-card")

    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, ".product-name").text
            price = int(item.find_element(By.CSS_SELECTOR, ".price").text.replace("₽", "").replace(" ", ""))
            product_url = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            # Фильтрация по цене и цвету
            if min_price <= price <= max_price and color.lower() in name.lower():
                products.append({
                    "name": name,
                    "price": price,
                    "url": product_url,
                })
        except:
            continue

    driver.quit()
    return products
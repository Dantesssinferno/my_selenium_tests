import time
from decimal import Decimal, ROUND_HALF_UP

from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================

BROWSER = 'chrome'
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--guest')
prefs = {
    "translate": {"enable": False},
    "intl.accept_languages": "en,en_US"
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--lang=en')
driver = webdriver.Chrome(options=chrome_options)
base_url = 'https://www.saucedemo.com/'
driver.get(base_url)
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)

# ===================== TEST DATA =====================
# Users
login_standard_user = 'standard_user'
password_universal = 'secret_sauce'

# Login form
login_field_xpath = "//input[@name='user-name']"
pass_field_xpath = "//input[@id='password']"
login_button_xpath = "//input[@id='login-button']"

# Product 1 (Backpack)
product_1_title_xpath = "//a[@id='item_4_title_link']"  # Sauce Labs Backpack
product_1_price_xpath = "(//div[@data-test='inventory-item-price'])[1]"
product_1_add_btn_xpath = "//button[@id='add-to-cart-sauce-labs-backpack']"

# Product 2 (Bike Light)
product_2_title_xpath = "//div[contains(text(), 'Sauce Labs Bike Light')]"
product_2_price_xpath = "(//div[@data-test='inventory-item-price'])[2]"
product_2_add_btn_xpath = "//button[@id='add-to-cart-sauce-labs-bike-light']"

# Cart / Checkout
cart_link_xpath = "//a[@class='shopping_cart_link']"
cart_checkout_xpath = "//button[@id='checkout']"

first_name_xpath = "//input[@id='first-name']"
last_name_xpath = "//input[@id='last-name']"
postal_code_xpath = "//input[@id='postal-code']"
continue_xpath = "//input[@id='continue']"

# Overview page
overview_item_titles_xpath = "//div[@class='inventory_item_name']"
overview_item_prices_xpath = "//div[@data-test='inventory-item-price']"
item_total_xpath = "//div[@class='summary_subtotal_label']"

# Finish
finish_button_xpath = "//button[@id='finish']"
thank_you_header_xpath = "//h2[@class='complete-header']"
back_home_button_xpath = "//button[@id='back-to-products']"

# Sample user data
first_name_value = "Maxim"
last_name_value = "Starostenko"
postal_code_value = "MD-5400"

# ===================== HELPERS =====================
def money(text: str) -> Decimal:
    """
    '$29.99' -> Decimal('29.99'), округление до копеек.
    """
    clean = text.strip().replace('$', '').replace(',', '')
    return Decimal(clean).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def parse_item_total_label(label_text: str) -> Decimal:
    """
    'Item total: $39.98' -> Decimal('39.98').
    """
    part = label_text.split(':', 1)[1].strip()
    return money(part)

def user_login(user_login_value: str, login_input_xpath: str) -> None:
    wait.until(EC.presence_of_element_located((By.XPATH, login_input_xpath)))
    driver.find_element(By.XPATH, login_input_xpath).send_keys(user_login_value)
    time.sleep(3)
    print('Шаг 1.1: Ввод логина — OK')

def user_password(password_value: str, pass_input_xpath: str) -> None:
    wait.until(EC.presence_of_element_located((By.XPATH, pass_input_xpath)))
    driver.find_element(By.XPATH, pass_input_xpath).send_keys(password_value)
    time.sleep(3)
    print('Шаг 1.2: Ввод пароля — OK')

def button_login(login_btn_xpath: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, login_btn_xpath)))
    driver.find_element(By.XPATH, login_btn_xpath).click()
    time.sleep(2)
    print('Шаг 1.3: Клик по Login — OK')
    # Проверим, что авторизовались (url inventory.html)
    wait.until(EC.url_contains("inventory.html"))
    print('Шаг 1.4: Проверка URL inventory — OK')

def read_product(title_xpath: str, price_xpath: str) -> tuple[str, str]:
    wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
    title = driver.find_element(By.XPATH, title_xpath).text
    wait.until(EC.presence_of_element_located((By.XPATH, price_xpath)))
    price = driver.find_element(By.XPATH, price_xpath).text
    print(f"Шаг 2: Прочитан товар: '{title}', цена: '{price}' — OK")
    return title, price

def add_to_cart(add_btn_xpath: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, add_btn_xpath)))
    driver.find_element(By.XPATH, add_btn_xpath).click()
    time.sleep(2)
    print("Шаг 3: Добавление товара в корзину — OK")

def open_cart(cart_xpath: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, cart_xpath)))
    driver.find_element(By.XPATH, cart_xpath).click()
    time.sleep(2)
    wait.until(EC.url_contains("cart.html"))
    print("Шаг 4: Переход в корзину — OK")

def checkout_cart(checkout_xpath: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, checkout_xpath)))
    driver.find_element(By.XPATH, checkout_xpath).click()
    time.sleep(2)
    wait.until(EC.url_contains("checkout-step-one.html"))
    print("Шаг 5: Нажат Checkout — OK")

def fill_user_info(first_x: str, last_x: str, post_x: str, cont_x: str) -> None:
    wait.until(EC.visibility_of_element_located((By.XPATH, first_x)))
    driver.find_element(By.XPATH, first_x).send_keys(first_name_value)
    time.sleep(1)
    print("Шаг 6.1: Ввод First Name — OK")

    wait.until(EC.visibility_of_element_located((By.XPATH, last_x)))
    driver.find_element(By.XPATH, last_x).send_keys(last_name_value)
    time.sleep(1)
    print("Шаг 6.2: Ввод Last Name — OK")

    wait.until(EC.visibility_of_element_located((By.XPATH, post_x)))
    driver.find_element(By.XPATH, post_x).send_keys(postal_code_value)
    time.sleep(1)
    print("Шаг 6.3: Ввод Postal Code — OK")

    wait.until(EC.element_to_be_clickable((By.XPATH, cont_x)))
    driver.find_element(By.XPATH, cont_x).click()
    time.sleep(1)
    wait.until(EC.url_contains("checkout-step-two.html"))
    print("Шаг 6.4: Переход на Overview — OK")

def read_overview_items(titles_x: str, prices_x: str) -> tuple[list[str], list[str]]:
    """
    Возвращает списки названий и цен (строки с $) на шаге Overview.
    """
    wait.until(EC.presence_of_all_elements_located((By.XPATH, titles_x)))
    title_els = driver.find_elements(By.XPATH, titles_x)
    titles = [el.text for el in title_els]

    wait.until(EC.presence_of_all_elements_located((By.XPATH, prices_x)))
    price_els = driver.find_elements(By.XPATH, prices_x)
    prices = [el.text for el in price_els]

    print(f"Шаг 7: Overview — позиции: {titles}")
    print(f"Шаг 7.1: Overview — цены: {prices}")
    return titles, prices

def read_item_total(label_xpath: str) -> str:
    wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))
    text = driver.find_element(By.XPATH, label_xpath).text
    print(f"Шаг 8: Label Item total: '{text}' — OK")
    return text

def click_finish_and_verify(finish_x: str, header_x: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, finish_x)))
    driver.find_element(By.XPATH, finish_x).click()
    wait.until(EC.url_contains("checkout-complete.html"))
    print("Шаг 10: Нажатие Finish — OK")

    wait.until(EC.visibility_of_element_located((By.XPATH, header_x)))
    header_text = driver.find_element(By.XPATH, header_x).text.strip()
    print(f"Шаг 10.1: Текст после Finish: '{header_text}' — OK")
    assert header_text == "Thank you for your order!", \
        f"Ожидали 'Thank you for your order!', получили '{header_text}'"
    print("Шаг 10.2: Проверка текста 'Thank you for your order!' — PASSED")

def click_back_home(back_home_x: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, back_home_x)))
    driver.find_element(By.XPATH, back_home_x).click()
    wait.until(EC.url_contains("inventory.html"))
    print("Шаг 11: Кнопка Back Home — OK (возврат в каталог)")

# ===================== TEST FLOW =====================

def run_tests() -> None:
    # 1) ЛОГИН
    user_login(login_standard_user, login_field_xpath)
    user_password(password_universal, pass_field_xpath)
    button_login(login_button_xpath)

    # 2) ЧТЕНИЕ ДВУХ ТОВАРОВ ИЗ КАТАЛОГА
    name1, price1 = read_product(product_1_title_xpath, product_1_price_xpath)  # Backpack
    name2, price2 = read_product(product_2_title_xpath, product_2_price_xpath)  # Bike Light

    # 2.1) СКЛАДЫВАЕМ СУММУ ДВУХ ТОВАРОВ (ПРОСТО)
    sum_two = (money(price1) + money(price2)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    print(f"Шаг 2.2: Сумма двух товаров: {money(price1)} + {money(price2)} = {sum_two}")

    # 3) ДОБАВЛЯЕМ ОБА ТОВАРА В КОРЗИНУ И ОТКРЫВАЕМ ЕЁ
    add_to_cart(product_1_add_btn_xpath)
    add_to_cart(product_2_add_btn_xpath)
    open_cart(cart_link_xpath)

    # 4) CHECKOUT STEP-ONE (ввод данных)
    checkout_cart(cart_checkout_xpath)
    fill_user_info(first_name_xpath, last_name_xpath, postal_code_xpath, continue_xpath)

    # 5) OVERVIEW: ЧИТАЕМ ПОЗИЦИИ И ЦЕНЫ, СВЕРЯЕМ НАЗВАНИЯ И СУММУ
    overview_titles, overview_prices = read_overview_items(
        overview_item_titles_xpath, overview_item_prices_xpath
    )

    # Проверка, что оба выбранных названия присутствуют
    assert name1.strip() in [t.strip() for t in overview_titles], \
        f"На Overview нет товара: '{name1}'"
    assert name2.strip() in [t.strip() for t in overview_titles], \
        f"На Overview нет товара: '{name2}'"
    print("Шаг 7.2: Проверка названий на Overview — PASSED")

    # Сумма всех цен, показанных на Overview
    overview_sum = sum(money(p) for p in overview_prices).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    print(f"Шаг 7.3: Сумма на Overview по видимым позициям: {overview_sum}")

    # Читаем Item total и сравниваем три значения
    item_total_label = read_item_total(item_total_xpath)
    item_total_value = parse_item_total_label(item_total_label)
    print(f"Шаг 9: Система говорит Item total = {item_total_value}")

    assert overview_sum == item_total_value == sum_two, \
        f"Несовпадение сумм: overview_sum={overview_sum}, item_total={item_total_value}, our_sum={sum_two}"
    print("Шаг 9.1: Проверка суммы (две цены vs Item total) — PASSED")

    # 6) FINISH и ПРОВЕРКА "THANK YOU..."
    click_finish_and_verify(finish_button_xpath, thank_you_header_xpath)

    # 7) BACK HOME
    click_back_home(back_home_button_xpath)

    print("\n=== ТЕСТ ПРОЙДЕН УСПЕШНО ===")

# ===================== ENTRYPOINT =====================
try:
    run_tests()
    print("\n[OK] run_tests() завершился без ошибок")
finally:
    # если тест упал - закроем окно браузера
    time.sleep(1)
    try:
        driver.quit()
    except Exception:
        pass
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================================================= BROWSER SETUP ======================================================
BROWSER = 'chrome'  # поменяй на "firefox", чтобы запустить Firefox

if BROWSER == 'chrome':
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--guest')
    prefs = {
        "translate": {"enable": False},
        "intl.accept_languages": "en,en_US"
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--lang=en")
    driver = webdriver.Chrome(options=chrome_options)

elif BROWSER == 'firefox':
    firefox_options = FirefoxOptions()
    firefox_options.set_preference("browser.translations.enable", False)
    firefox_options.set_preference("intl.accept_languages", "en-US, en")
    # firefox_options.add_argument("-headless")
    firefox_options.add_argument("-width=1440")
    firefox_options.add_argument("-height=860")
    driver = webdriver.Firefox(options=firefox_options)

else:
    raise ValueError("BROWSER должен быть 'chrome' или 'firefox'")

base_url = 'https://www.saucedemo.com/'
driver.get(base_url)

try:
    driver.set_window_size(1440, 860)
except Exception:
    pass

wait = WebDriverWait(driver, 10)

# =================================================== TEST DATA ========================================================
# Users
login_standard_user = 'standard_user'
login_locked_out_user = 'locked_out_user'
login_problem_user = 'problem_user'
login_performance_glitch_user = 'performance_glitch_user'
login_error_user = 'error_user'
login_visual_user = 'visual_user'

# Password
password_universal = 'secret_sauce'

# XPaths (логичные имена с суффиксом _xpath)
burger_button_xpath = "//button[@id='react-burger-menu-btn']"
burger_about_button_xpath = "//a[@id='about_sidebar_link']"

login_field_xpath = "//input[@name='user-name']"
pass_field_xpath = "//input[@id='password']"
login_button_xpath = "//input[@id='login-button']"

# Старые локаторы на 1-й товар
product_1_xpath = "//a[@id='item_4_title_link']"
price_prod_1_xpath = "//div[@class='inventory_item_price'][1]"
select_prod_1_xpath = "//button[@id='add-to-cart-sauce-labs-backpack']"

cart_link_xpath = "//a[@class='shopping_cart_link']"

cart_product_1_xpath = "//div[@class='inventory_item_name'][1]"
cart_price_prod_1_xpath = "//div[@class='inventory_item_price'][1]"

cart_checkout_xpath = "//button[@id='checkout']"

first_name_xpath = "//input[@id='first-name']"
last_name_xpath = "//input[@id='last-name']"
postal_code_xpath = "//input[@id='postal-code']"

first_name_value = "Maxim"
last_name_value = "Starostenko"
postal_code_value = "MD-5400"

continue_xpath = "//input[@id='continue']"

# Обновлённые общие локаторы для overview
checkout_overview_title_xpath = "//div[@data-test='inventory-item-name']"
checkout_overview_price_xpath = "//div[@data-test='inventory-item-price']"

item_total_xpath = "//div[@class='summary_subtotal_label']"
finish_checkout_xpath = "//button[@id='finish']"
finish_txt_xpath = "//h2[@data-test='complete-header']"
back_home_xpath = "//button[@id='back-to-products']"

# Локаторы для каталога через CSS
inventory_item_css = ".inventory_item"
inventory_item_name_css = ".inventory_item_name"
inventory_item_price_css = ".inventory_item_price"
inventory_item_button_css = "button.btn_inventory"

# ============================================= STEPS ==================================================================
def user_login(user_login_value: str, login_input_xpath: str) -> None:
    wait.until(EC.presence_of_element_located((By.XPATH, login_input_xpath)))
    user_name_el = driver.find_element(By.XPATH, login_input_xpath)
    user_name_el.send_keys(user_login_value)
    print('Шаг: 1: Input Login : success')

def user_password(password_value: str, pass_input_xpath: str) -> None:
    wait.until(EC.presence_of_element_located((By.XPATH, pass_input_xpath)))
    user_pass_el = driver.find_element(By.XPATH, pass_input_xpath)
    user_pass_el.send_keys(password_value)
    print('Шаг: 1.1: Input password : success')

def button_login(login_btn_xpath: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, login_btn_xpath)))
    driver.find_element(By.XPATH, login_btn_xpath).click()
    print('Шаг: 1.2: Login button clicked : success')
    time.sleep(1)

def read_all_products() -> list[dict]:
    """
    Считывает все товары на странице каталога и возвращает список словарей:
    {
        "index": 1,
        "title": "...",
        "price": "...",
        "button": <WebElement кнопки Add to cart>
    }
    """
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, inventory_item_css)))
    items = driver.find_elements(By.CSS_SELECTOR, inventory_item_css)

    products: list[dict] = []
    print("Шаг: 2: Найдены товары в каталоге:")
    for idx, item in enumerate(items, start=1):
        title_el = item.find_element(By.CSS_SELECTOR, inventory_item_name_css)
        price_el = item.find_element(By.CSS_SELECTOR, inventory_item_price_css)
        button_el = item.find_element(By.CSS_SELECTOR, inventory_item_button_css)

        title_text = title_el.text
        price_text = price_el.text

        products.append(
            {
                "index": idx,
                "title": title_text,
                "price": price_text,
                "button": button_el,
            }
        )
        print(f"  {idx}. {title_text} - {price_text}")

    print(f"Всего товаров: {len(products)}")
    return products


def ask_user_choice(products: list[dict]) -> dict:
    """
    Спрашивает у пользователя номер товара, пока не будет введён корректный номер.
    Возвращает словарь с выбранным товаром из списка products.
    """
    max_index = len(products)
    while True:
        choice_str = input(f"Введите номер товара, который хотите заказать (1-{max_index}): ").strip()

        if not choice_str.isdigit():
            print("Нужно ввести число. Попробуйте ещё раз.")
            continue

        choice = int(choice_str)
        if 1 <= choice <= max_index:
            chosen_product = products[choice - 1]
            print(
                f"Вы выбрали товар №{choice}: "
                f"{chosen_product['title']} - {chosen_product['price']}"
            )
            return chosen_product
        else:
            print(f"Неверный номер. Введите число от 1 до {max_index}.")


def read_product_1(title_xpath: str, price_xpath: str) -> tuple[str, str]:
    # сейчас не используется, оставил для совместимости
    wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
    title_el = driver.find_element(By.XPATH, title_xpath)
    value_title = title_el.text
    print(f"Шаг: 2: {value_title}")

    wait.until(EC.presence_of_element_located((By.XPATH, price_xpath)))
    price_el = driver.find_element(By.XPATH, price_xpath)
    value_price = price_el.text
    print(f"Шаг: 2.1: {value_price}")

    return value_title, value_price


def select_prod_by_button(button_element) -> None:
    wait.until(EC.element_to_be_clickable(button_element))
    button_element.click()
    print("Шаг: 3: Selected product: Passed")


def open_cart(cart_xpath: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, cart_xpath)))
    driver.find_element(By.XPATH, cart_xpath).click()
    print("Шаг: 4: Enter cart: Passed")


def cart_info(title_xpath: str, price_xpath: str) -> tuple[str, str]:
    wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
    cart_title_el = driver.find_element(By.XPATH, title_xpath)
    cart_title = cart_title_el.text
    print(f"Шаг: 5: {cart_title}")

    wait.until(EC.presence_of_element_located((By.XPATH, price_xpath)))
    cart_price_el = driver.find_element(By.XPATH, price_xpath)
    cart_price = cart_price_el.text
    print(f"Шаг: 6: {cart_price}")
    time.sleep(1)
    return cart_title, cart_price


def checkout_cart(cart_checkout_xpath: str) -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, cart_checkout_xpath)))
    driver.find_element(By.XPATH, cart_checkout_xpath).click()
    print("Шаг: 7: Checkout button clicked : success")
    time.sleep(1)


def select_user_info(first_name_xpath, last_name_xpath, postal_code_xpath, continue_xpath):
    wait.until(EC.visibility_of_element_located((By.XPATH, first_name_xpath)))
    first_name_el = driver.find_element(By.XPATH, first_name_xpath)
    first_name_el.send_keys(first_name_value)  # Maxim
    print("Шаг: 8.1: input first name: success")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.XPATH, last_name_xpath)))
    last_name_el = driver.find_element(By.XPATH, last_name_xpath)
    last_name_el.send_keys(last_name_value)  # Starostenko
    print("Шаг: 8.2: input last name: success")
    time.sleep(1)

    wait.until(EC.visibility_of_element_located((By.XPATH, postal_code_xpath)))
    postal_code_el = driver.find_element(By.XPATH, postal_code_xpath)
    postal_code_el.send_keys(postal_code_value)  # MD-5400
    print("Шаг: 8.3: input postal code: success")
    time.sleep(1)

    wait.until(EC.element_to_be_clickable((By.XPATH, continue_xpath)))
    driver.find_element(By.XPATH, continue_xpath).click()
    print("Шаг: 8.4: Continue button clicked: success")
    wait.until(EC.url_contains("checkout-step-two.html"))


def checkout_overview(checkout_overview_title_xpath: str,
                      checkout_overview_price_xpath: str) -> tuple[str, str]:
    wait.until(EC.presence_of_element_located((By.XPATH, checkout_overview_title_xpath)))
    checkout_overview_title_el = driver.find_element(By.XPATH, checkout_overview_title_xpath)
    checkout_overview_title_text = checkout_overview_title_el.text
    print(f"Шаг: 9.1: {checkout_overview_title_text}")

    wait.until(EC.presence_of_element_located((By.XPATH, checkout_overview_price_xpath)))
    checkout_overview_price_el = driver.find_element(By.XPATH, checkout_overview_price_xpath)
    checkout_overview_price_text = checkout_overview_price_el.text
    print(f"Шаг: 9.2: {checkout_overview_price_text}")

    return checkout_overview_title_text, checkout_overview_price_text


def item_total_sum(item_total_xpath: str) -> str:
    """Возвращает строку вида 'Item total: $29.99' и печатает её."""
    wait.until(EC.presence_of_element_located((By.XPATH, item_total_xpath)))
    total_sum_el = driver.find_element(By.XPATH, item_total_xpath)
    total_sum_text = total_sum_el.text
    print(f"Шаг: 10: {total_sum_text}")
    return total_sum_text


def finish_checkout(finish_checkout: str, finish_txt: str) -> str:
    wait.until(EC.element_to_be_clickable((By.XPATH, finish_checkout_xpath)))
    driver.find_element(By.XPATH, finish_checkout_xpath).click()
    print("Шаг: 11: Finish Checkout button clicked : success")
    time.sleep(1)

    finish_txt_el = wait.until(EC.visibility_of_element_located((By.XPATH, finish_txt_xpath)))
    finish_txt_text = finish_txt_el.text
    print(f"Шаг: 11.1: Finish text {finish_txt_text}")
    time.sleep(1)
    return finish_txt_text


def back_home() -> str:
    wait.until(EC.element_to_be_clickable((By.XPATH, back_home_xpath)))
    driver.find_element(By.XPATH, back_home_xpath).click()
    print("Шаг: 12: Back home button clicked : success")
    time.sleep(1)

    wait.until(EC.url_contains("inventory.html"))
    catalog_url = driver.current_url
    print(f"Шаг: 12.1: Current URL is: {catalog_url}")
    return catalog_url

# ==================================================== TEST FLOW =======================================================
def run_tests() -> None:
    # 1) Логин/пароль
    user_login(login_standard_user, login_field_xpath)
    user_password(password_universal, pass_field_xpath)
    button_login(login_button_xpath)

    # 2) Чтение всех товаров из каталога и выбор пользователем
    products = read_all_products()
    chosen = ask_user_choice(products)

    # 3) Сохраняем имя и цену выбранного товара из каталога
    name_catalog = chosen["title"]
    price_catalog = chosen["price"]

    # 4) Добавление выбранного товара в корзину и переход в корзину
    select_prod_by_button(chosen["button"])
    open_cart(cart_link_xpath)

    # 5) Чтение товара и цены из корзины
    name_cart, price_cart = cart_info(cart_product_1_xpath, cart_price_prod_1_xpath)

    # 6) Сравнение (assert'ы с выводом)
    assert name_catalog.strip() == name_cart.strip(), \
        f"Имя товара не совпало: '{name_catalog}' vs '{name_cart}'"
    print("Шаг: 6.1: Name catalog = name cart: Passed")

    assert price_catalog.strip() == price_cart.strip(), \
        f"Цена товара не совпала: '{price_catalog}' vs '{price_cart}'"
    print("Шаг: 6.2: Price catalog = price cart: Passed")

    # 7) Нажать Checkout
    checkout_cart(cart_checkout_xpath)

    # 8) Ввести имя, фамилию, почтовый индекс и перейти дальше
    select_user_info(first_name_xpath, last_name_xpath, postal_code_xpath, continue_xpath)

    # 9) Checkout: Overview повторная проверка позиции и цены
    overview_title, overview_price = checkout_overview(
        checkout_overview_title_xpath,
        checkout_overview_price_xpath
    )

    # 10) Вывод на печать итоговой суммы по позициям без учета налога
    total_summ_text = item_total_sum(item_total_xpath)

    # 11) Сравнение (assert'ы с выводом)
    assert name_cart.strip() == overview_title.strip(), \
        f"Имя товара не совпало: '{name_cart}' vs '{overview_title}'"
    print("Шаг: 10.1: Name cart = name checkout overview: Passed")

    assert price_cart.strip() == overview_price.strip(), \
        f"Цена товара не совпала: '{price_cart}' vs '{overview_price}'"
    print("Шаг: 10.2: Price cart = price checkout overview: Passed")

    # 12) Finish заказ
    finish_text = finish_checkout(finish_checkout_xpath, finish_txt_xpath)

    # 13) URL Back home
    back_home_url = back_home()

    print("Тест завершён успешно.")
    print("Финальное сообщение:", finish_text)
    print("URL каталога после Back home:", back_home_url)

# ======================================================= ENTRYPOINT ===================================================
run_tests()

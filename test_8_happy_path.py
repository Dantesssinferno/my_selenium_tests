import time
from idlelib.colorizer import color_config

from cffi.model import char_array_type
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""INFO browser"""
BROWSER = 'chrome'  # поменяй на "chrome" чтобы запустить Chrome

if BROWSER == 'chrome':  # запускаем Chrome
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

"""INFO users"""
login_standard_user = 'standard_user'
login_locked_out_user = 'locked_out_user'
login_problem_user = 'problem_user'
login_performance_glitch_user = 'performance_glitch_user'
login_error_user = 'error_user'
login_visual_user = 'visual_user'
"""INFO users password"""
password_universal = 'secret_sauce'
"""INFO burger buttons"""
burger_button = "//button[@id='react-burger-menu-btn']"
burger_about_button = "//a[@id='about_sidebar_link']"
"""INFO login_fields"""
login_field = "//input[@name='user-name']"
pass_field = "//input[@id='password']"
"""INFO login button"""
login_button = "//input[@id='login-button']"
"""INFO product_1"""
product_1 = "//a[@id='item_4_title_link']"
price_prod_1 = "//div[@class='inventory_item_price'][1]"
"""SELECT product_1"""
select_prod_1 = "//button[@id='add-to-cart-sauce-labs-backpack']"
"""Cart"""
cart_loc = "//a[@class='shopping_cart_link']"
# Сохраняем копию строкового XPath ДО объявления одноимённой функции
product_1_xpath_copy = product_1
"""INFO cart product_1"""
cart_product_1 = "//div[@class='inventory_item_name'][1]"
cart_price_prod_1 = "//div[@class='inventory_item_price'][1]"

try:
    driver.set_window_size(1440, 860)
except Exception:
    pass

wait = WebDriverWait(driver, 10)

# Ищем поле логин и вводим логин
def user_login(login_standard_user, login_field):
    wait.until(EC.presence_of_element_located((By.XPATH, login_field)))
    user_name = driver.find_element(By.XPATH, login_field)
    user_name.send_keys(login_standard_user)
    print('Input Login : success')

# Ищем поле пароль и вводим пароль
def user_password(password_universal, pass_field):
    wait.until(EC.presence_of_element_located((By.XPATH, pass_field)))
    user_pass = driver.find_element(By.XPATH, pass_field)
    user_pass.send_keys(password_universal)
    print('Input password : success')

# Ждём кнопку логина и кликаем
def button_login(login_button):
    wait.until(EC.element_to_be_clickable((By.XPATH, login_button)))
    driver.find_element(By.XPATH, login_button).click()  # <-- реальный клик
    print('Login button clicked : success')
    time.sleep(1)

# Находим товар и его цену
def product_1(product_1, price_prod_1):
    # product_1 здесь — строка XPATH
    wait.until(EC.presence_of_element_located((By.XPATH, product_1)))
    find_prod_1 = driver.find_element(By.XPATH, product_1)         # <-- 2 позиционных аргумента
    value_prod_1 = find_prod_1.text                                # <-- читаем у WebElement
    print(value_prod_1)
    wait.until(EC.presence_of_element_located((By.XPATH, price_prod_1)))
    find_price_prod_1 = driver.find_element(By.XPATH, price_prod_1) # <-- 2 позиционных аргумента
    value_price_prod_1 = find_price_prod_1.text
    print(value_price_prod_1)
    # >>> ВОЗВРАЩАЕМ имя и цену из каталога <<<
    return value_prod_1, value_price_prod_1

def select_prod(select_prod_1):
    wait.until(EC.element_to_be_clickable((By.XPATH, select_prod_1)))
    driver.find_element(By.XPATH, select_prod_1).click()
    print("Selected prod: Passed")

def cart(cart_loc):
    wait.until(EC.element_to_be_clickable((By.XPATH, cart_loc)))
    driver.find_element(By.XPATH, cart_loc).click()
    print("Enter cart: Passed")

def cart_info(cart_product_1, cart_price_prod_1):
    # product_1 здесь — строка XPATH
    wait.until(EC.presence_of_element_located((By.XPATH, cart_product_1)))
    cart_find_prod_1 = driver.find_element(By.XPATH, cart_product_1)         # <-- 2 позиционных аргумента
    cart_value_prod_1 = cart_find_prod_1.text                                # <-- читаем у WebElement
    print(cart_value_prod_1)
    wait.until(EC.presence_of_element_located((By.XPATH, cart_price_prod_1)))
    cart_find_price_prod_1 = driver.find_element(By.XPATH, cart_price_prod_1) # <-- 2 позиционных аргумента
    cart_value_price_prod_1 = cart_find_price_prod_1.text
    print(cart_value_price_prod_1)
    # >>> ВОЗВРАЩАЕМ имя и цену из корзины <<<
    return cart_value_prod_1, cart_value_price_prod_1

def run_tests(login_standard_user, password_universal, product_1):
    user_login(login_standard_user, login_field)
    user_password(password_universal, pass_field)
    button_login(login_button)
    # Передаём строковый XPath через сохранённую копию
    name_catalog, price_catalog = product_1(product_1_xpath_copy, price_prod_1)
    select_prod(select_prod_1)
    cart(cart_loc)
    name_cart, price_cart = cart_info(cart_product_1, cart_price_prod_1)
    # 4) СРАВНЕНИЕ — ВОТ ЗДЕСЬ СТАВИМ ASSERT
    assert name_catalog.strip() == name_cart.strip(), \
    f"Имя товара не совпало: '{name_catalog}' vs '{name_cart}'"
    print("Name catalog = name cart: Passed")
    assert price_catalog.strip() == price_cart.strip(), \
    f"Цена товара не совпала: '{price_catalog}' vs '{price_cart}'"
    print("Price catalog = price cart: Passed")
# Запуск
run_tests(login_standard_user, password_universal, product_1)

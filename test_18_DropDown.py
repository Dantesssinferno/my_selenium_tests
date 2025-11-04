import tempfile
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--lang=en')

# 1) Чистый профиль на каждый запуск (надёжнее, чем реальный профиль)
user_data_dir = tempfile.mkdtemp(prefix="selenium-chrome-profile-")
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.add_argument('--no-first-run')
chrome_options.add_argument('--no-default-browser-check')
chrome_options.add_argument('--disable-sync')
chrome_options.add_argument('--incognito')  # инкогнито дополнительно гасит сохранение паролей

# 2) Правильные prefs для паролей и утечек
prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "translate": {"enable": False},
    "intl.accept_languages": "en,en_US",

    # ВАЖНО: корректные ключи
    "credentials_enable_service": False,     # отключает Google Password Manager
    "profile.password_manager_enabled": False,  # не предлагает сохранить
    "password_manager_leak_detection": False    # не проверяет на утечки
}
chrome_options.add_experimental_option('prefs', prefs)

# 3) Флаги отключения соответствующих фич
chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding,EnablePasswordsAccountStorage,SafeBrowsingEnhancedProtection,AutofillServerCommunication,PasswordStrengthIndicator")
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

BASE_URL = "https://www.saucedemo.com/"
driver.get(BASE_URL)

# ===================== LOCATORS =====================
# Users
login_standard_user = 'standard_user'

# Password
password_universal = 'secret_sauce'

# Fields
login_field_xpath = "//input[@name='user-name']"
pass_field_xpath = "//input[@id='password']"
login_button_xpath = "//input[@id='login-button']"
select_dropdown_1_xpath = "//select[@class='product_sort_container']"


# ===================== ВСПОМОГАТЕЛЬНЫЕ ДАННЫЕ =====================
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
    wait.until(EC.url_contains("inventory.html"))
    wait.until(EC.visibility_of_element_located((By.XPATH, select_dropdown_1_xpath)))

def dropdown():
    select = Select(wait.until(EC.visibility_of_element_located((By.XPATH, select_dropdown_1_xpath))))
    print("Шаг: 2: Dropdown located")
    select.select_by_visible_text("Name (Z to A)")
    print("Шаг: 2.1: Name (Z to A), selected")
    select = Select(wait.until(EC.visibility_of_element_located((By.XPATH, select_dropdown_1_xpath))))
    select.select_by_value("lohi")
    print("Шаг: 2.2: Price (low to high), selected")
    select = Select(wait.until(EC.visibility_of_element_located((By.XPATH, select_dropdown_1_xpath))))
    select.select_by_visible_text("Price (high to low)")
    print("Шаг: 2.3: Price (high to low), selected")
    select = Select(wait.until(EC.visibility_of_element_located((By.XPATH, select_dropdown_1_xpath))))
    select.select_by_visible_text("Name (A to Z)")
    print("Шаг: 2.4: Name (A to Z), selected")

# ===================== Запуск =====================
try:
    user_login(login_standard_user, login_field_xpath)
    user_password(password_universal, pass_field_xpath)
    button_login(login_button_xpath)
    dropdown()
finally:
    # driver.quit() # включить в CI
    pass
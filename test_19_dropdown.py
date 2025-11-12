import tempfile
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

BASE_URL = "https://www.lambdatest.com/selenium-playground/jquery-dropdown-search-demo"
driver.get(BASE_URL)

# ===================== LOCATORS =====================
# Fields
select_country_below_xpath = "//span[@class='select2-selection select2-selection--single']"
# Country
select_USA_xpath = "(//li[@class='select2-results__option'])[10]"
# Input (устойчивый локатор без индекса)
input_country_xpath = "//input[contains(@class,'select2-search__field')]"
# Выбранный текст
selected_text_xpath = "//span[contains(@class,'select2-selection__rendered')]"
japan_text_xpath = "//li[contains(@class,'select2-results__option')][7]"

# ===================== ВСПОМОГАТЕЛЬНЫЕ ДАННЫЕ =====================
def open_dropdown():
    # Нахожу список стран по локатору и раскрываю его
    finde_drop_el = wait.until(EC.element_to_be_clickable((By.XPATH, select_country_below_xpath)))
    finde_drop_el.click()
    print(f"Finde_drop_el: Located and clicked")

    # Выбираю страну USA
    usa_el = wait.until(EC.element_to_be_clickable((By.XPATH, select_USA_xpath)))
    usa_el.click()
    print(f"Country: USA selected")

    # Проверка
    rendered = wait.until(EC.visibility_of_element_located((By.XPATH, selected_text_xpath)))
    assert "United States" in rendered.text or "USA" in rendered.text, \
    f"Unexpected selected: {rendered.text}"

def write_dropdown():
    # Снова открываю список стран
    input_country_el = wait.until(EC.element_to_be_clickable((By.XPATH, select_country_below_xpath)))
    input_country_el.click()
    print(f"Input_country: Located and clicked")

    # Ввожу текст в поле поиска Select2
    input_country_el = wait.until(EC.visibility_of_element_located((By.XPATH, input_country_xpath)))
    input_country_el.clear()
    input_country_el.send_keys("Japan")
    print(f"Input_country: Japan and clicked")

    # Явно выбираю нужную страну
    japan_el = wait.until(EC.element_to_be_clickable((By.XPATH, japan_text_xpath.format("Japan"))))
    japan_el.click()

    # Проверка
    rendered = wait.until(EC.visibility_of_element_located((By.XPATH, selected_text_xpath)))
    assert "Japan" in rendered.text, \
    f"Expected Japan, got: {rendered.text}"
    print(f"Country selected: {rendered.text}")

# ===================== Запуск =====================
try:
    open_dropdown()
    write_dropdown()
finally:
    # driver.quit() # включить в CI
    pass
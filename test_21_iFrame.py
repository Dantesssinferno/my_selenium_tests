import tempfile
from typing import KeysView

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--lang=en')

user_data_dir = tempfile.mkdtemp(prefix="selenium-chrome-profile-")
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.add_argument('--no-first-run')
chrome_options.add_argument('--no-default-browser-check')
chrome_options.add_argument('--disable-sync')
chrome_options.add_argument('--incognito')

prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "translate": {"enable": False},
    "intl.accept_languages": "en,en_US",
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "password_manager_leak_detection": False
}
chrome_options.add_experimental_option('prefs', prefs)

chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding,EnablePasswordsAccountStorage")
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

BASE_URL = "https://www.lambdatest.com/selenium-playground/iframe-demo/"
driver.get(BASE_URL)

# ===================== LOCATORS =====================
iframe_id_xpath = "//iframe[@id='iFrame1']"
editor_xpath = "//div[@class='rsw-ce' and @contenteditable='true']"  # единый локатор редактора
bold_el_xpath = "//button[@title='Bold']"
italic_al_xpath = "//button[@title='Italic']"
strike_through_xpath = "//button[@title='Strike through']"  # фикс
underline_xpath = "//button[@title='Underline']"

# ===================== STEPS =====================
def iframe():
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_id_xpath)))
    print("iframe detected and swiched")

def input_field():
    iframe_input_field_el = wait.until(EC.presence_of_element_located((By.XPATH, editor_xpath)))
    print("✅ Simple iFrame editor detected")
    return iframe_input_field_el

def iframe_input(iframe_input_field_el):
    # 3️⃣ Вводим текст
    iframe_input_field_el.send_keys("Hello from Selenium!")
    print("✍️ Text successfully sent")

    # 📄 Текст до редактирования
    old_txt = iframe_input_field_el.text
    print("📄 Text in editor (before):", old_txt)

    # 4️⃣ Жирный шрифт
    iframe_input_field_el.send_keys(Keys.CONTROL, 'a')   # чуть надёжнее, чем '+'
    bold_button = wait.until(EC.element_to_be_clickable((By.XPATH, bold_el_xpath)))
    bold_button.click()
    print("Bold clicked")

    # 📄 Текст после редактирования — заново находим редактор и берём .text
    new_el = wait.until(EC.visibility_of_element_located((By.XPATH, editor_xpath)))
    new_txt = new_el.text
    print("📄 Text in editor (after):", new_txt)

    # 5️⃣ Сравниваем строки
    assert old_txt == new_txt, f"Ожидался {old_txt}, но получили {new_txt}"
    print(f"✅ Тексты равны: '{old_txt}' == '{new_txt}'")

    # 6️⃣ Остальные клики (по желанию)
    wait.until(EC.element_to_be_clickable((By.XPATH, italic_al_xpath))).click()
    print("Italic clicked")
    wait.until(EC.element_to_be_clickable((By.XPATH, strike_through_xpath))).click()
    print("Strike through clicked")
    wait.until(EC.element_to_be_clickable((By.XPATH, underline_xpath))).click()
    print("Underline clicked")

# ===================== RUN =====================
iframe()
field_iframe = input_field()
iframe_input(field_iframe)
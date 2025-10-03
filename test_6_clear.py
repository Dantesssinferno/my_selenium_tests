import time
from datetime import datetime, UTC
from pathlib import Path
from typing import KeysView

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# -------------------- Настройки --------------------
BROWSER = 'chrome'
LOGIN = 'standard_user'
PASSWORD = 'secret_sauce'
# Локаторы (кортежи удобнее и безопаснее)
LOC_USER_NAME       = (By.ID, "user-name")
LOC_USER_PASS       = (By.ID, "password")
LOC_LOGIN_BTN       = (By.ID, "login-button")
LOC_ONESIE_ADD_BTN  = (By.ID, "add-to-cart-sauce-labs-onesie")
LOC_RED_TSHIRT_BTN  = (By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)")
BASE_URL = "https://www.saucedemo.com/"
SCREEN_DIR = Path(r"C:\Users\Maxim Starostenco\PycharmProjects\my_selenium_tests\screen")

def sanitize_for_filename(s: str) -> str:
    return "".join(c if (c.isalnum() or c in ('-', '_')) else '_' for c in s)
# -------------------- Инициализация драйвера --------------------
if BROWSER == 'chrome':
    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument('--guest')
    chrome_options.add_experimental_option("prefs", {
        "translate": {"enable": False},
        "intl.accept_languages": "en,en_US"
    })
    chrome_options.add_argument("--lang=en")
    driver = webdriver.Chrome(options=chrome_options)

elif BROWSER == 'firefox':
    firefox_options = FirefoxOptions()
    firefox_options.set_preference("browser.translations.enable", False)
    firefox_options.set_preference("intl.accept_languages", "en-US, en")
    firefox_options.add_argument("-width=1440")
    firefox_options.add_argument("-height=860")
    driver = webdriver.Firefox(options=firefox_options)

else:
    raise ValueError("BROWSER должен быть 'chrome' или 'firefox'")
driver.get(BASE_URL)
driver.set_window_size(1440, 860)

wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)
SCREEN_DIR.mkdir(parents=True, exist_ok=True)

# -------------------- Логин --------------------
el_user = wait.until(EC.visibility_of_element_located(LOC_USER_NAME))
el_user.send_keys(LOGIN)
print("Input Login : success")

# Небольшая пауза просто "чтобы увидеть", можно убрать
time.sleep(5)
el_user.clear() # clear() - это самый простой способ для очистки полей, правда он может сработать не всегда, поэтому будем так же рассматривать и альтернативы

# -------------------- Логин --------------------
el_user = wait.until(EC.visibility_of_element_located(LOC_USER_NAME))
el_user.send_keys(LOGIN)
print("Input Login : success")
# Небольшая пауза просто "чтобы увидеть", можно убрать
time.sleep(5)
el_user.send_keys(Keys.CONTROL + 'a') # выделяем содержимое поля
el_user.send_keys(Keys.DELETE) # удаляем выделенный текст при помощи DELETE

# -------------------- Логин --------------------
el_user = wait.until(EC.visibility_of_element_located(LOC_USER_NAME))
el_user.send_keys(LOGIN)
print("Input Login : success")
# Небольшая пауза просто "чтобы увидеть", можно убрать
time.sleep(5)
el_user.send_keys(Keys.CONTROL + 'a') # выделяем содержимое поля
el_user.send_keys(Keys.BACKSPACE) # удаляем выделенный текст при помощи BACKSPACE

# el_pass = wait.until(EC.visibility_of_element_located(LOC_USER_PASS))
# el_pass.send_keys(PASSWORD)
# print("Input password : success")
#
# wait.until(EC.element_to_be_clickable(LOC_LOGIN_BTN)).click()
# print("Login button clicked : success")




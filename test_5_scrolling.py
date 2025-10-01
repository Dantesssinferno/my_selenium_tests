import time
from datetime import datetime, UTC
from pathlib import Path

from selenium import webdriver
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

el_pass = wait.until(EC.visibility_of_element_located(LOC_USER_PASS))
el_pass.send_keys(PASSWORD)
print("Input password : success")

wait.until(EC.element_to_be_clickable(LOC_LOGIN_BTN)).click()
print("Login button clicked : success")

# Небольшая пауза просто "чтобы увидеть", можно убрать
time.sleep(1)

# -------------------- 1) Onesie: скролл + скрин --------------------
onesie_btn = wait.until(EC.presence_of_element_located(LOC_ONESIE_ADD_BTN))
actions.move_to_element(onesie_btn).perform()
time.sleep(1)

slug1 = onesie_btn.get_attribute("id") or "sauce-labs-onesie"
name1 = f"screenshot_{sanitize_for_filename(slug1)}_{datetime.now(UTC).strftime('%Y.%m.%d.%H.%M.%S')}.png"

# Вариант A: весь экран
driver.save_screenshot(str(SCREEN_DIR / name1))
# Вариант B (точечно элемент): onesie_btn.screenshot(str(SCREEN_DIR / name1))

print(f"Screenshot saved: success {name1}")

# -------------------- 2) Red T-Shirt: скролл + скрин --------------------
red_btn = wait.until(EC.presence_of_element_located(LOC_RED_TSHIRT_BTN))
actions.move_to_element(red_btn).perform()
time.sleep(1)

slug2 = red_btn.get_attribute("id") or "test-allthethings-t-shirt-red"
name2 = f"screenshot_{sanitize_for_filename(slug2)}_{datetime.now(UTC).strftime('%Y.%m.%d.%H.%M.%S')}.png"

driver.save_screenshot(str(SCREEN_DIR / name2))
# Или точечно: red_btn.screenshot(str(SCREEN_DIR / name2))

print(f"Screenshot saved: success {name2}")

# При необходимости:
# driver.quit()
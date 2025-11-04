import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True) # не закрывать окно после завершения скрипта
chrome_options.add_argument('--lang=en') # язык интерфейса браузера
chrome_options.add_argument("--disable-features=PrivacySandboxSettings4,UserDataConsent")
chrome_options.add_argument("--disable-popup-blocking")
prefs = {
    "profile.default_content_setting_values.cookies": 2,  # 2 = блокировать cookies
    "profile.default_content_setting_values.notifications": 2,
    "translate": {"enable": False}, # отключить автоперевод страниц
    "intl.accept_languages": "en,en_US" # запрашиваем контент/форматы en-US
}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=chrome_options)
BASE_URL = "https://html5css.ru/howto/howto_js_rangeslider.php"
driver.get(BASE_URL)
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)
try:
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fc-button fc-cta-do-not-consent fc-secondary-button']")))
    btn.click()
    print("✅ Cookie banner closed automatically")
except:
    print("ℹ️ Cookie banner not found — continuing")
action = ActionChains(driver)

# ===================== LOCATORS =====================
default_rangeslider_xpath = "//input[@type='range']"
square_rangeslider_xpath = "//input[@class='slider-square']"
round_rangeslider_xpath = "//input[@class='slider-color']"
value_image_xpath = "//input[@class='slider-pic']"

# ===================== ВСПОМОГАТЕЛЬНЫЕ ДАННЫЕ =====================
def default_slider_run():
    default_slider_el = wait.until(EC.element_to_be_clickable((By.XPATH, default_rangeslider_xpath)))
    action.click_and_hold(default_slider_el).move_by_offset(150, 0).release().perform()
    print("Default slider moved")
    time.sleep(3)

def square_slider_run():
    square_slider_el = wait.until(EC.element_to_be_clickable((By.XPATH, square_rangeslider_xpath)))
    action.click_and_hold(square_slider_el).move_by_offset(350, 0).release().perform()
    print("Square slider moved")
    time.sleep(3)

def round_slider_run():
    round_slider_el = wait.until(EC.element_to_be_clickable((By.XPATH, round_rangeslider_xpath)))
    action.click_and_hold(round_slider_el).move_by_offset(480, 0).release().perform()
    print("Round slider moved")
    time.sleep(3)

def value_slider_run():
    value_slider_run_el = wait.until(EC.element_to_be_clickable((By.XPATH, value_image_xpath)))
    action.click_and_hold(value_slider_run_el).move_by_offset(500,0).release().perform()
    print("Value slider moved")
    time.sleep(3)

# ===================== Запуск =====================
default_slider_run()
square_slider_run()
round_slider_run()
value_slider_run()
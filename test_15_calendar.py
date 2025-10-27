import time
from datetime import datetime, UTC

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--guest')
prefs = {
    "translate": {"enable": False},
    "intl.accept_languages": "en,en_US"
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--lang=en')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://demoqa.com/date-picker')
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

# ===================== LOCATORS =====================
new_date_xpath = "//input[@id='datePickerMonthYearInput']"
day_29_xpath = "//div[contains(@class,'react-datepicker__day') and not(contains(@class,'outside-month')) and text()='29']"
today_xpath = "//div[contains(@class, 'react-datepicker__day--today')]"
now_date = datetime.now(UTC).strftime("%Y.%m.%d.%H.%M.%S")
# ===================== STEPS =====================

def new_date():
    # очистка и ввод руками
    new_date_el = wait.until(EC.element_to_be_clickable((By.XPATH, new_date_xpath)))
    print(f"'new_date_el': located")
    new_date_el.send_keys(Keys.CONTROL,"a")
    new_date_el.send_keys(Keys.DELETE)
    print(f"'new_date_el': cleared")
    time.sleep(3)
    new_date_el.send_keys('10/28/2025')
    new_date_el.send_keys(Keys.RETURN)
    time.sleep(1)


def new_date_2():
    # выбор через выпадающий календарь
    input_el_date_2 = wait.until(EC.element_to_be_clickable((By.XPATH, new_date_xpath)))
    input_el_date_2.click() # ОТКРЫВАЕМ календарь

    # ждём попап календаря
    input_el_date_2 = wait.until(EC.visibility_of_element_located((By.XPATH, day_29_xpath)))
    print(f"'29 october 2025': located")
    input_el_date_2.click() # ОТКРЫВАЕМ календарь
    print(f"'29 october 2025': clicked")

def today():
    # открыть календарь (если закрыт)
    input_el = wait.until(EC.element_to_be_clickable((By.XPATH, new_date_xpath)))
    input_el.click()
    # дождаться появления дня "сегодня"
    today_el = wait.until(EC.element_to_be_clickable((By.XPATH, today_xpath)))
    today_el.click()
    # today_value = driver.find_element(By.XPATH, new_date_xpath).get_attribute("value")
    # print(f"Текущая дата в поле: {today_value}")
    print(f"Now date: {now_date}")



new_date()
new_date_2()
today()
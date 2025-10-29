import time
from datetime import datetime, UTC, timedelta

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True) # не закрывать окно после завершения скрипта
chrome_options.add_argument('--guest') # чистый гость-профиль без кук/истории
prefs = {
    "translate": {"enable": False}, # отключить автоперевод страниц
    "intl.accept_languages": "en,en_US" # запрашиваем контент/форматы en-US
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--lang=en') # язык интерфейса браузера

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://demoqa.com/date-picker')
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

# ===================== LOCATORS =====================
today_date_xpath = "//input[@id='datePickerMonthYearInput']"

# ===================== ВСПОМОГАТЕЛЬНЫЕ ДАННЫЕ =====================
# Текущее UTC-время в формате Г.М.Д.Ч.М.С
now_date = datetime.now(UTC).strftime("%Y.%m.%d.%H.%M.%S")

def date_plus_10_days() -> str:
    # Выводим текущее локальное время
    print(f"Now date: {now_date}")
    # Берем локальное текущее время и прибавляем 10 дней
    target_date = datetime.now(UTC) + timedelta(days=10)
    target_date_str = target_date.strftime("%m/%d/%Y")
    # Выводим ожидаемое время +10 дней
    print(f"Target date + 10 days: {target_date_str}")
    return target_date_str

def select_date() -> WebElement:
    # поиск поля Select Date
    today_date_el = wait.until(EC.element_to_be_clickable((By.XPATH, today_date_xpath)))
    today_date_el.click()
    print(f"'Select Date': located")
    # очищаем поле Select Date
    today_date_el.send_keys(Keys.CONTROL, "a")
    today_date_el.send_keys(Keys.DELETE)
    print(f"'Select Date': cleared")
    return today_date_el

def input_target_date(today_date_el: WebElement, target_date_str: str) -> None:
    # Вводим ожидаемое время +10 дней
    today_date_el.send_keys(target_date_str)
    today_date_el.send_keys(Keys.RETURN)
    time.sleep(3)
    actual_date_value = today_date_el.get_attribute("value")
    assert actual_date_value == target_date_str, \
    f"Ожидал {target_date_str}, но получил {actual_date_value}"
    print(f"Ожидаемая дата {target_date_str} = Актуальной дате {actual_date_value}")

# ===================== Запуск =====================
target_date_str = date_plus_10_days() # сохраняю возвращаемое значение
today_date_el = select_date() # сохранить возвращаемое значение
input_target_date(today_date_el, target_date_str) # передаю аргументы явно

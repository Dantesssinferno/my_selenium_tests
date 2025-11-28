import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
#=============================================================BROWSER_SETUP==============================================

# инициилизируем chrome_options
chrome_options = webdriver.ChromeOptions()
# оставить окно открытым после завершения скрипта (удобно при обучении)
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument('--headless') # запуск теста в безголовом режиме, не запуская окно браузера
# 🔑 запуск в гостевом режиме
# chrome_options.add_argument('--guest')
# 🔑 отключаем переводчик и выставляем язык
prefs = {
     "intl.accept_languages": "en,en_US"
 }
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--lang=en")
g = Service()
driver = webdriver.Chrome(options=chrome_options, service=g)
driver.get("https://demoqa.com/radio-button")
wait = WebDriverWait(driver, 3)
driver.maximize_window()

#=============================================================LOCATORS==================================================
yesRadio_xpath = "//label[@for='yesRadio']"
yes_message_xpath = "//span[@class='text-success']"
value_massage = "Yes"
#=============================================================STEPS=====================================================
def click_yes_radio():
    # Пытаемся сразу найти сообщение (вдруг уже кликнуто)
    try:
        el_yes_message = driver.find_element(By.XPATH, yes_message_xpath)
        print("STEP 1: yes_message located (without click)")
        el_yes_message_txt = el_yes_message.text
    except NoSuchElementException as exception:
        print("NoSuchElementException message not found, clicking radio...")
        # Кликаем по радио
        el_yes_radio = driver.find_element(By.XPATH, yesRadio_xpath)
        print("STEP 2: yesRadio located")
        el_yes_radio.click()
        print("STEP 3: yesRadio clicked")
        # Ждём появления сообщения ПОСЛЕ клика
        el_yes_message = wait.until(EC.visibility_of_element_located((By.XPATH, yes_message_xpath)))
        print("STEP 4: yes_message located after click")
        el_yes_message_txt = el_yes_message.text
    print(f"STEP 5: text = {el_yes_message_txt}")
    assert el_yes_message_txt == value_massage, \
        f"Ожидал текст '{value_massage}', а получил '{el_yes_message_txt}'"
#=============================================================RUN=======================================================
click_yes_radio()


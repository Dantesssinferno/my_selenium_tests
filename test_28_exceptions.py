import time
from selenium import webdriver
from selenium.common import NoSuchElementException
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
driver.get("https://demoqa.com/dynamic-properties")
wait = WebDriverWait(driver, 3)
driver.maximize_window()

#=============================================================LOCATORS==================================================
button_will_enable_5_sec_xpath = "//button[@id='visibleAfter']"
#=============================================================STEPS=====================================================
def click_button_visible_after_5_sec():
    # Нахожу кнопку download_file и нажимаю ее
    try:
        el_download_file = driver.find_element(By.XPATH, button_will_enable_5_sec_xpath)
        print("STEP 1: Button visible after 5 sec located")
        el_download_file.click()
        print("STEP 2: Button visible after 5 sec clicked")
    except NoSuchElementException as exception:
        print("NoSuchElementException")
        time.sleep(10)
        el_download_file = driver.find_element(By.XPATH, button_will_enable_5_sec_xpath)
        print("STEP 1: Button visible after 5 sec located")
        el_download_file.click()
        print("STEP 2: Button visible after 5 sec clicked")

#=============================================================RUN=======================================================
click_button_visible_after_5_sec()


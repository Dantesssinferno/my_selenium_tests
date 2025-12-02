from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
wait = WebDriverWait(driver, 10)
#driver.maximize_window()
# waiting = driver.implicitly_wait(3) # неявное ожидание
#=============================================================LOCATORS==================================================
button_will_enable_5_sec_xpath = "//button[@id='visibleAftero']"
button_visible_after_5_sec_xpath = "//button[@id='visibleAfter']"
#=============================================================STEPS=====================================================
def click_btn():
    print("Start Test")
    # waiting_el = waiting
    # Пытаемся сразу найти сообщение кнопку
    el_will_enable_5_sec = driver.find_element(By.XPATH, button_will_enable_5_sec_xpath)
    print("STEP 1: btn located")
    el_yes_message_txt = el_will_enable_5_sec.text
    print("Finish Test")

def click_btn_2():
    print("Start Test")
    # Пытаемся сразу найти сообщение кнопку
    el_will_enable_5_sec = wait.until(EC.element_to_be_clickable((By.XPATH, button_visible_after_5_sec_xpath)))
    print("STEP 1: btn located")
    el_yes_message_txt = el_will_enable_5_sec.text
    print(f"Finish Test: {el_yes_message_txt}")

#=============================================================RUN=======================================================
# click_btn()
click_btn_2()

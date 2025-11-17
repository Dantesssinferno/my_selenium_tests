import time

import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait


#=============================================================BROWSERSETUP==============================================
chrome_options = webdriver.ChromeOptions()
# оставить окно открытым после завершения скрипта (удобно при обучении)
chrome_options.add_experimental_option('detach', True)
# # chrome_options.add_argument('--headless') # запуск теста в безголовом режиме, не запуская окно браузера
# # 🔑 запуск в гостевом режиме
# chrome_options.add_argument('--guest')
# # 🔑 отключаем переводчик и выставляем язык
# prefs = {
#     "translate": {"enable": False},
#     "intl.accept_languages": "en,en_US"
# }
# chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument("--lang=en")
g = Service()
driver = webdriver.Chrome(options=chrome_options, service=g)
driver.get("https://demoqa.com/browser-windows")
wait = WebDriverWait(driver, 10)
driver.maximize_window()
time.sleep(3)

#=============================================================LOCATORS==================================================
tab_button = "//button[@id='tabButton']"
header_1 = "//h1[@class='text-center']"

#=============================================================STEPS=====================================================
def click_new_tab():
    new_tab_click = wait.until(EC.element_to_be_clickable((By.XPATH, tab_button)))
    new_tab_click.click()
    print(f"NEW TAB BUTTON: LOCATED AND CLICKED")
    time.sleep(3)
    print(driver.current_url)

    header_page_1 = wait.until(EC.presence_of_element_located((By.XPATH, header_1))).text
    page_1_txt = header_page_1
    print(f"text page 1: {header_page_1}")



#=============================================================RUN=======================================================
click_new_tab()
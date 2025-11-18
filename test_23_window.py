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
header_2 = "//h1[@id='sampleHeading']"
window_button = "//button[@id='windowButton']"
window_2_title = "//h1[@id='sampleHeading']"
#=============================================================STEPS=====================================================
def click_new_tab():
    new_tab_click = wait.until(EC.element_to_be_clickable((By.XPATH, tab_button)))
    new_tab_click.click()
    print(f"ШАГ.1 NEW TAB BUTTON: LOCATED AND CLICKED")
    time.sleep(3)
    print(f"ШАГ.1.1 {driver.current_url}")

    header_page_1 = wait.until(EC.presence_of_element_located((By.XPATH, header_1))).text
    page_1_txt = header_page_1
    print(f"ШАГ.2 TEXT ON PAGE 1: {page_1_txt}")

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    print(f"ШАГ.2.1 {driver.current_url}")

    header_page_2 = wait.until(EC.presence_of_element_located((By.XPATH, header_2))).text
    page_2_txt = header_page_2
    print(f"ШАГ.3 TEXT ON PAGE 2: {page_2_txt}")

    driver.switch_to.window(driver.window_handles[0])
    print(f"ШАГ.3.1 {driver.current_url}")
    return page_1_txt


def click_new_window(page_1_txt:str) -> str:
    # Находим кнопку New window
    new_window_click = wait.until(EC.element_to_be_clickable((By.XPATH, window_button)))
    # Нажимаем кнопку New window
    new_window_click.click()
    print(f"ШАГ.4 NEW WINDOW BUTTON: LOCATED AND CLICKED")
    time.sleep(3)
    # Показываем текущую ссылку
    print(f"ШАГ.4.1 {driver.current_url}")

    # Переменные которые помогут перемещаться по окнам
    windows_1 = driver.window_handles[0]
    windows_2 = driver.window_handles[1]

    # Перемещаемся в окно 2
    driver.switch_to.window(windows_2)
    # Находим заголовок во втором окне
    title_text_win_2 = wait.until(EC.presence_of_element_located((By.XPATH, window_2_title))).text
    # Помещаем в переменную текст из второго окна
    win_2_txt = title_text_win_2
    # Печатаем текст из окна 2
    print(f"ШАГ.5 Title on window 2: {win_2_txt}")
    # Перемещаемся в окно 1
    driver.switch_to.window(windows_1)
    #
    print(f"ШАГ.5.1 {driver.current_url}")
    print(f"ШАГ.5.2 {page_1_txt}")

#=============================================================RUN=======================================================
page_1_txt = click_new_tab()
click_new_window(page_1_txt)
print("Test: PASSED")
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service


#=============================================================BROWSER_SETUP==============================================
chrome_options = webdriver.ChromeOptions()
# оставить окно открытым после завершения скрипта (удобно при обучении)
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument('--headless') # запуск теста в безголовом режиме, не запуская окно браузера
# 🔑 запуск в гостевом режиме
chrome_options.add_argument('--guest')
# 🔑 отключаем переводчик и выставляем язык
prefs = {
     "translate": {"enable": False},
     "intl.accept_languages": "en,en_US"
 }
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--lang=en")
g = Service()
driver = webdriver.Chrome(options=chrome_options, service=g)
driver.get("https://the-internet.herokuapp.com/javascript_alerts")
wait = WebDriverWait(driver, 10)
driver.maximize_window()
time.sleep(3)

#=============================================================LOCATORS==================================================
js_alert_xpath = "//button[@onclick='jsAlert()']"
result_txt_alert_xpath = "//p[@id='result']"
js_alert_confirm_xpath = "//button[@onclick='jsConfirm()']"
result_txt_alert_confirm_xpath = "//p[@id='result']"


#=============================================================STEPS=====================================================
# Взаимодействие с ALERT у которого только кнопка OK
def click_alert():
    # Нахожу кнопку alert и нажимаю ее
    el_alert = wait.until(EC.element_to_be_clickable((By.XPATH, js_alert_xpath)))
    el_alert.click()
    # Вывожу на печать, если локатор alert найден
    print(f"ШАГ.1 Alert element: LOCATED AND CLICKED")
    time.sleep(3)
    # Переключаем driver в окно alert и нажимаем единственную кнопку accept()
    driver.switch_to.alert.accept()
    # Считываем текст который подтверждает успех закрытия алерта
    el_successfully_clicked_an_alert = wait.until(EC.presence_of_element_located((By.XPATH, result_txt_alert_xpath))).text
    expected_text = "You successfully clicked an alert"
    text_actual = el_successfully_clicked_an_alert
    assert text_actual == expected_text, \
    f"Ожидали получить {expected_text}, но получили {text_actual}"
    print(f"ШАГ.2 Result: {text_actual}")

# Взаимодействие с ALERT у которого кнопка OK и Cancel
def click_alert_confirm(action: str):
    """
    action: 'accept' -> нажать OK
            'dismiss' -> нажать Cancel
    """
    # 1. Открываем confirm
    el_alert_confirm = wait.until(EC.element_to_be_clickable((By.XPATH, js_alert_confirm_xpath)))
    el_alert_confirm.click()
    # Вывожу на печать, если локатор alert confirm найден
    print(f"ШАГ.3 Alert confirm element: LOCATED AND CLICKED")
    time.sleep(1)
    # 2. Получаем объект alert один раз
    alert_confirm = driver.switch_to.alert
    driver.switch_to.alert.send_keys("test")
    # 3. Ветвление логики по выбранному действию
    if action == "accept":
        alert_confirm.accept()
        expected_text = "You clicked: Ok"
        print("НАЖАЛИ: OK (accept)")
    elif action == "dismiss":
        alert_confirm.dismiss()
        expected_text = "You clicked: Cancel"
        print("НАЖАЛИ: Cancel (dismiss)")
    else:
        raise ValueError(f"Неизвестное действие для alert: {action}")

    # 4. Читаем текст результата на странице
    el_result = wait.until(EC.presence_of_element_located((By.XPATH, result_txt_alert_confirm_xpath))).text
    text_actual = el_result

    assert text_actual == expected_text, \
        f"Ожидали получить {expected_text}, но получили {text_actual}"
    print(f"ШАГ.4 Result: {text_actual}")
#=============================================================RUN=======================================================
click_alert()

# Вариант 1: тестируем нажатие OK
click_alert_confirm("accept")

# Вариант 2: тестируем нажатие Cancel
click_alert_confirm("dismiss")
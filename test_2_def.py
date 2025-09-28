import time
from idlelib.colorizer import color_config
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==== ПЕРЕМЕННЫЕ ====
base_url = 'https://www.saucedemo.com/'

login_standard_user = 'standard_use'  # сломан login_standard_user для негативного тестирования
login_locked_out_user = 'locked_out_user'  # юзер заблокирован — проверяем корректный текст ошибки
login_problem_user = 'problem_user'
login_performance_glitch_user = 'performance_glitch_user'
login_error_user = 'error_user'
login_visual_user = 'visual_user'
password_universal = 'secret_sauce'
# ======================================
# ==== Локаторы ====
login = "//input[@name='user-name']"
password = "//input[@id='password']"
login_button = "//input[@id='login-button']"
warring_pop_up = "//h3[@data-test='error']"
# ======================================

def browser_run():
    # спрашиваем у пользователя
    BROWSER = input("Выбери браузер (chrome/firefox): ").strip().lower()

    if BROWSER == 'chrome': # запускаем Chrome
        chrome_options = ChromeOptions()
        # оставить окно открытым после завершения скрипта (удобно при обучении)
        chrome_options.add_experimental_option('detach', True)
        # chrome_options.add_argument('--headless') # запуск теста в безголовом режиме, не запуская окно браузера
        # 🔑 запуск в гостевом режиме
        chrome_options.add_argument('--guest')
        # 🔑 отключаем переводчик и выставляем язык
        prefs = {
            "translate":{"enable": False},
            "intl.accept_languages":"en,en_US"
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--lang=en")
        driver = webdriver.Chrome(options=chrome_options)

    elif BROWSER == 'firefox':
        firefox_options = FirefoxOptions()
        # Firefox не имеет аналога detach; окно остаётся, пока процесс жив
        # отключаем встроенный переводчик Firefox
        firefox_options.set_preference("browser.translations.enable", False)
        firefox_options.set_preference("intl.accept_languages", "en-US, en")
        # ВАЖНО: headless и размер окна — ДО создания драйвера
        # firefox_options.add_argument("-headless")  # включаем headless
        firefox_options.add_argument("-width=1440")
        firefox_options.add_argument("-height=860")
        driver = webdriver.Firefox(options=firefox_options)

    else:
        # на всякий случай — дефолт в chrome
        print("Неизвестный браузер. Использую chrome по умолчанию.")
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        chrome_options.add_argument('--guest')
        prefs = {
            "translate": {"enable": False},
            "intl.accept_languages": "en,en_US"
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--lang=en")
        drv = webdriver.Chrome(options=chrome_options)
        # В headless maximize_window может быть бесполезен/ломать — используем set_window_size на всякий случай
    try:
        driver.set_window_size(1440, 860)
    except Exception:
        pass
    driver.get(base_url)
    return driver
    # создаю драйвер один раз на основе выбора юзера
driver = browser_run()

def open_login_page():
    driver.get(base_url)
    time.sleep(1)

def input_credentials(user_name):
    # Ищем поле логин и вводим логин
    username = driver.find_element(By.XPATH, login)  # ID XPATH
    username.clear()  # очистим поле логин, если в нем уже что-то есть
    username.send_keys(user_name)  # заполняем поле логин данными user_name
    print('Input Login : success')

    # Ищем поле пароль и вводим пароль
    user_pass = driver.find_element(By.XPATH, password)
    user_pass.clear()
    user_pass.send_keys(password_universal)
    print('Input password : success')

def click_login():
    # Ищем кнопку логин и кликаем кнопку, ставлю слипы, для того чтобы, увидеть как проходит тест
    time.sleep(1) # чтобы увидеть результат
    button_login = driver.find_element(By.XPATH, login_button)
    button_login.click()
    print('Login button clicked : success')
    time.sleep(2) # чтобы увидеть результат

def check_negative(expected_text):
    warring_text = driver.find_element(By.XPATH, warring_pop_up)
    actual_value_warring_text = warring_text.text
    assert actual_value_warring_text == expected_text, f"Ожидался: {expected_text}, получили: {actual_value_warring_text}"
    print("Negative login test: Passed")

def check_positive():
    # успех — страница инвентаря или заголовок Products (.title)
    success = ('inventory' in driver.current_url) or bool(driver.find_element(By.CLASS_NAME, "title"))
    assert success, "Ожидали успешный вход, но не увидели страницу товара."
    print("Positive login test: Passed")

def logout_if_possible():
    # логаут для следующего кейса
    try:
        time.sleep(1)
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        driver.find_element(By.ID, "logout_sidebar_link").click()
        time.sleep(1)
    except Exception:
        pass

def run_case(user_name, expect_error, expected_text):
    print(f'===========Test user: {user_name}===========')
    open_login_page()
    input_credentials(user_name)
    click_login()

    try:
        if expect_error:
            check_negative(expected_text)
        else:
            check_positive()
            # logout_if_possible()
    except (AssertionError, NoSuchElementException) as e:
        print(f"❌ Negative login test FAILED for {user_name}: {e}")
        failures.append((user_name, str(e)))

# Какие результаты ждем от каждого юзера
test_cases = [
    #(логин, ожидается_ошибка(True/False), текст ошибки если есть)
    (login_standard_user, True, 'Epic sadface: Username and password do not match any user in this service'),
    (login_locked_out_user, True, 'Epic sadface: Sorry, this user has been locked out.'),
    (login_problem_user, False, ''),
    (login_performance_glitch_user, False, ''),
    (login_error_user, False, ''),
    (login_visual_user, False, '')
]

failures = []

for user_name, expect_error, expected_text in test_cases:
    run_case(user_name, expect_error, expected_text)

if failures:
    print("\nИтоги: есть проваленные кейсы: ")
    for u, reason in failures:
        print(f" - {u}: {reason}")
else:
    print("\nИтоги: все кейсы пройдены ✅")
# оставляем браузер открытым из-за detach; при желании закрыть — раскомментировать
# driver.quit()

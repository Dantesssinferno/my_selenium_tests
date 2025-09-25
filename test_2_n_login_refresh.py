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


BROWSER = 'chrome' # поменяй на "chrome" чтобы запустить Chrome

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
    raise ValueError("BROWSER должен быть 'chrome' или 'firefox'")
base_url = 'https://www.saucedemo.com/'
driver.get(base_url)
# В headless maximize_window может быть бесполезен/ломать — используем set_window_size на всякий случай
try:
    driver.set_window_size(1440, 860)
except Exception:
    pass
login_standard_user = 'standard_use' # сломан login_standard_user для негативного тестирования
login_locked_out_user = 'locked_out_user'
login_problem_user = 'problem_user'
login_performance_glitch_user = 'performance_glitch_user'
login_error_user = 'error_user'
login_visual_user = 'visual_user'
password_universal = 'secret_sauce'

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
    print(f'===========Test user: {user_name}===========')
    driver.get(base_url)
    time.sleep(1)

    # Ищем поле логин и вводим логин
    username = driver.find_element(By.XPATH,"//input[@name='user-name']") # ID XPATH
    username.clear() # очистим поле логин, если в нем уже что-то есть
    username.send_keys(user_name) # заполняем поле логин данными user_name
    print('Input Login : success')

    # Ищем поле пароль и вводим пароль
    user_pass = driver.find_element(By.XPATH, "//input[@id='password']")
    user_pass.clear()
    user_pass.send_keys(password_universal)
    print('Input password : success')

    # Ищем кнопку логин и кликаем кнопку, ставлю слипы, для того чтобы, увидеть как проходит тест
    time.sleep(1) # чтобы увидеть результат
    button_login = driver.find_element(By.XPATH, "//input[@id='login-button']")
    button_login.click()
    print('Login button clicked : success')
    time.sleep(2) # чтобы увидеть результат

    if expect_error:
        # ------ ОБЕРНУТО В try/except ------
        try:
            # негативный тест: проверяем текст ошибки
            warring_text = driver.find_element(By.XPATH, "//h3[@data-test='error']")
            actual_value_warring_text = warring_text.text
            assert actual_value_warring_text == expected_text, \
                f"Ожидался: {expected_text}, получили: {actual_value_warring_text}"
            print("Negative login test: Passed")
        except (AssertionError, NoSuchElementException) as e:
            print(f"❌ Negative login test FAILED for {user_name}: {e}")
            failures.append((user_name, str(e)))
            # -----------------------------------
    else:
        # ------ ОБЕРНУТО В try/except ------
        try:
            # позитивный тест: считаем успехом появление страницы инвентаря (по URL или заголовку Products)
            success = ('inventory' in driver.current_url) or bool(driver.find_element(By.CLASS_NAME, "title"))
            assert success, "Ожидали успешный вход, но не увидели страницу товара."
            print("Positive login test: Passed")

            # простой логаут (чтобы следующий кейс стартовал с логина)
            try:
                time.sleep(1)
                driver.find_element(By.ID, "react-burger-menu-btn").click()
                time.sleep(1)
                driver.find_element(By.ID, "logout_sidebar_link").click()
                time.sleep(1)
            except Exception:
                pass
        except (AssertionError, NoSuchElementException) as e:
            print(f"❌ Positive login test FAILED for {user_name}: {e}")
            failures.append((user_name, str(e)))


# (необязательно) краткий итог
if failures:
    print("\nИтоги: есть проваленные кейсы:")
    for u, reason in failures:
        print(f" - {u}: {reason}")
else:
    print("\nИтоги: все кейсы пройдены ✅")
# оставляем браузер открытым из-за detach; при желании закрыть — раскомментировать
# driver.quit()



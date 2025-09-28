import time
from idlelib.colorizer import color_config
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BROWSER = 'chrome' # поменяй на "chrome" чтобы запустить Chrome

login_standard_user = 'standard_user'
login_locked_out_user = 'locked_out_user'
login_problem_user = 'problem_user'
login_performance_glitch_user = 'performance_glitch_user'
login_error_user = 'error_user'
login_visual_user = 'visual_user'
password_universal = 'secret_sauce'

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

# Ищем поле логин и вводим, логин
user_name = driver.find_element(By.XPATH,"//input[@name='user-name']") # ID XPATH
user_name.send_keys(login_standard_user)
print('Input Login : success')

# Ищем поле пароль и вводим, пароль
user_pass = driver.find_element(By.XPATH, "//input[@id='password']")
user_pass.send_keys(password_universal)
print('Input password : success')
user_pass.send_keys(Keys.RETURN) # используется для замены клика по кнопке Login

# Ищем фильтр, кликаем на него, выбираем второй элемент и нажимаем Enter
filter = driver.find_element(By.XPATH, "//select[@data-test='product-sort-container']")
time.sleep(3)
filter.click()
print('Click Filter: success')
time.sleep(3)
filter.send_keys(Keys.DOWN)
time.sleep(3)
filter.send_keys(Keys.RETURN)


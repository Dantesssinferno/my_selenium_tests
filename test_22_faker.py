from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from faker import Faker



#=============================================================BROWSERSETUP===============================================
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

#==============================================LOCATORS==================================================================
password_universal = 'secret_sauce'
login = "//input[@name='user-name']"
password = "//input[@id='password']"
login_button = "//input[@id='login-button']"

#==============================================STEPS=====================================================================
# Генерируем рандомный логин и пароль
faker = Faker("en_US") # данные будут генерироваться на английском языке
rnd_name = faker.first_name() + str(faker.random_int(0,10000))
rnd_password = faker.password(15, True, True, True, True)
rndurl = faker.url()
print(f"{rndurl}")
print(f"{rnd_name}")
print(f"{rnd_password}")

def input_credentials():
    # Ищем поле логин и вводим логин
    username = driver.find_element(By.XPATH, login)  # ID XPATH
    username.clear()  # очистим поле логин, если в нем уже что-то есть
    username.send_keys(rnd_name)  # заполняем поле логин данными user_name
    print('Input Login : success')

    # Ищем поле пароль и вводим пароль
    user_pass = driver.find_element(By.XPATH, password)
    user_pass.clear()
    user_pass.send_keys(rnd_password)
    print('Input password : success')

#==============================================RUN=======================================================================
input_credentials()
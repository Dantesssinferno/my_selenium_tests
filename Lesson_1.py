import time
from selenium import webdriver
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
    driver = webdriver.Firefox(options=firefox_options)

else:
    raise ValueError("BROWSER должен быть 'chrome' или 'firefox'")

driver.get('https://www.saucedemo.com/')
driver.maximize_window()

# user_name = driver.find_element(By.ID, "user-name") # ID
# user_name = driver.find_element(By.NAME, "user-name") # NAME
# user_name = driver.find_element(By.XPATH,"//input[@id='user-name']") # FULL XPATH
user_name = driver.find_element(By.XPATH,"//*[@id='user-name']") # ID XPATH
# user_name = driver.find_element(By.XPATH, "//input[@data-test='username']") # data-test XPATH
user_name.send_keys("standard_user")

# user_pass = driver.find_element(By.ID, "password")
# user_pass.send_keys("secret_sauce")
#
# time.sleep(2)
# user_login = driver.find_element(By.ID, "login-button")
# user_login.click()
# time.sleep(3) # чтобы увидеть результат
# driver.quit()  # при detach=True у Chrome можно вызвать driver.quit() позже вручную






import time
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

BROWSER = 'chrome' # поменяй на "chrome" чтобы запустить Chrome

if BROWSER == 'chrome': # запускаем Chrome
    chrome_options = ChromeOptions()
    # оставить окно открытым после завершения скрипта (удобно при обучении)
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=chrome_options)

elif BROWSER == 'firefox':
    firefox_options = FirefoxOptions()
    # Firefox не имеет аналога detach; окно остаётся, пока процесс жив
    driver = webdriver.Firefox(options=firefox_options)

else:
    raise ValueError("BROWSER должен быть 'chrome' или 'firefox'")

driver.get('https://www.saucedemo.com/')
driver.maximize_window()
time.sleep(30) # чтобы увидеть результат
driver.quit()  # при detach=True у Chrome можно вызвать driver.quit() позже вручную






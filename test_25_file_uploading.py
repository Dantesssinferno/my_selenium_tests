import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
#=============================================================BROWSER_SETUP==============================================
# инициилизируем chrome_options
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
driver.get("https://www.lambdatest.com/selenium-playground/upload-file-demo")
wait = WebDriverWait(driver, 10)
driver.maximize_window()
time.sleep(3)
#=============================================================LOCATORS==================================================
uploading_file_xpath = "//input[@id='file']"
succsess_text_xpath = "//div[@id='error' and contains(text(), 'File Successfully Uploaded')]"
#=============================================================STEPS=====================================================
# Взаимодействие с ALERT у которого только кнопка OK
def click_button_uploading_file():
    # Прописываем абсолютный путь к загружаемому файлу
    path_upload = "C:\\Users\\Maxim Starostenco\\PycharmProjects\\my_selenium_tests\\file_uploading\\sampleFoto.jpg"
    # Нахожу кнопку uploading_file и нажимаю ее
    el_uploading_file = wait.until(EC.element_to_be_clickable((By.XPATH, uploading_file_xpath)))
    el_uploading_file.send_keys(path_upload)
    expected_succsess_text = "File Successfully Uploaded"
    actual_succsess_text = wait.until(EC.presence_of_element_located(((By.XPATH, succsess_text_xpath)))).text
    assert expected_succsess_text == actual_succsess_text, \
    f"Ожидали получить {expected_succsess_text}, но получили {actual_succsess_text}"
    print(f"Текст после загрузки файла: {expected_succsess_text}")
#=============================================================RUN=======================================================
click_button_uploading_file()

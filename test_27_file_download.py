import glob
import os.path
import time

from faker.providers.ssn.el_GR import tin_checksum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
#=============================================================BROWSER_SETUP==============================================
# переменная которая ссылается на дефолтный путь по которому будут скачиваться наши файлы
path_download = "C:\\Users\\Maxim Starostenco\\PycharmProjects\\my_selenium_tests\\files_download"
# инициилизируем chrome_options
chrome_options = webdriver.ChromeOptions()
# оставить окно открытым после завершения скрипта (удобно при обучении)
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument('--headless') # запуск теста в безголовом режиме, не запуская окно браузера
# 🔑 запуск в гостевом режиме
# chrome_options.add_argument('--guest')
# 🔑 отключаем переводчик и выставляем язык
prefs = {
     "download.default_directory": path_download,
     "translate": {"enable": False},
     "intl.accept_languages": "en,en_US"
 }
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--lang=en")
g = Service()
driver = webdriver.Chrome(options=chrome_options, service=g)
driver.get("https://www.lambdatest.com/selenium-playground/download-file-demo")
wait = WebDriverWait(driver, 10)
driver.maximize_window()
time.sleep(3)
#=============================================================LOCATORS==================================================
download_file_xpath = "//button[contains(text(), 'Download File')]"

#=============================================================STEPS=====================================================
def wait_for_file(file_path: str, timeout: int = 15) -> None:
    """
    Ждём, пока появится файл по указанному пути.
    Если не появился за timeout секунд — кидаем AssertionError.
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        if os.path.exists(file_path):
            return
        time.sleep(0.5)

    raise AssertionError(f"Файл {file_path} не был найден за {timeout} секунд")

def click_button_download_file_and_check():
    # Нахожу кнопку download_file и нажимаю ее
    el_download_file = wait.until(EC.element_to_be_clickable((By.XPATH, download_file_xpath)))
    el_download_file.click()
    print("STEP 1: Нажали кнопку 'Download File'")

    # директория не пустая
    # Ждём, пока файл LambdaTest.pdf появится в нужной папке
    if os.listdir(path_download):
        print("Файл в наличии")
    else:
        print("Файла нет")
    # содержимое директории
    print(os.listdir(path_download))

    # наличие требуемого файла в директории
    file_name = "LambdaTest.pdf"
    file_path = os.path.join(path_download, file_name)
    wait_for_file(file_path, timeout=15)
    print(f"Искомый файл {file_name} находится в директории: {file_path}")

    # файл не пуст
    files = glob.glob(os.path.join(path_download, "*.*"))
    for file in files:
        a = os.path.getsize(file)
        if a > 10:
            print("Файл не пуст")
        else:
            print("Файл пуст")

    # очистка директории
    files = glob.glob(os.path.join(path_download, "*.*"))
    for file in files:
        os.remove(file)
        print("Файл удален")
#=============================================================RUN=======================================================
click_button_download_file_and_check()

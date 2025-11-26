import glob
import os.path
import time
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
succsess_text_xpath = "//div[@id='error' and contains(text(), 'File Successfully Uploaded')]"
#=============================================================STEPS=====================================================
def wait_file_downloaded(download_dir: str, filename_part: str, timeout: int = 15) -> str:
    """
    Ждём, пока в папке скачиваний появится файл, в имени которого есть filename_part.
    Возвращаем полный путь к найденному файлу.
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        files = glob.glob(os.path.join(download_dir, "*"))
        for f in files:
            if filename_part in os.path.basename(f) and not f.endswith(".crdownload"):
                return f
            time.sleep(0.5)
    raise AssertionError(f"Файл с частью имени '{filename_part}' не был скачан за {timeout} секунд")

def click_button_download_file_and_check():
    # Нахожу кнопку download_file и нажимаю ее
    el_download_file = wait.until(EC.element_to_be_clickable((By.XPATH, download_file_xpath)))
    el_download_file.click()
    print("STEP 1: Нажали кнопку 'Download File'")

    # Ждём, пока файл LambdaTest.pdf появится в нужной папке
    downloaded_file = wait_file_downloaded(path_download, "LambdaTest")
    print(f"STEP 2: Файл скачан в каталог: {downloaded_file}")

    # Проверяем, что именно в НАШУ папку
    assert downloaded_file.startswith(path_download), (
        f"Файл скачан не в ожидаемую директорию. "
        f"Ожидали: {path_download}, получили: {downloaded_file}"
    )
    print("STEP 3: Подтверждено, что директория скачивания верная.")
#=============================================================RUN=======================================================
click_button_download_file_and_check()

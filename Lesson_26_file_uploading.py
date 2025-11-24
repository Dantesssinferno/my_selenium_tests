#   Привет Друзья!
#
# В данной лекции Мы научимся загружать файл в браузер. Данный функционал нам пригодится,
# когда нам необходимо, к примеру сымитировать ситуацией с прикладыванием требуемого файла
# во время прохождения бизнес процесса нашего приложения. Например при отправке сообщения в
# почтовом сервисе, конвертировании файлов, к примеру из pdf в jpg, загрузки фото в анкету и т.д.
#
# Перед Вами тестовый сайт, с подобным функционалом.
#
# Ссылка на ресурс - Upload File Demo Website | Selenium Playground | Run Selenium Test Online (lambdatest.com)
#
# Если Мы будем проходить данный сценарий вручную, то нам необходимо будет кликнуть на кнопку
# "Выбор файла", далее у нас появится соответствующее окно, с возможностью выбора файла.
# Но с данным окном Мы не сможем взаимодействовать с помощью WebDriver.
# Для этого нам понадобится уже знакомый нам метод send_keys().
#
# Для начала давайте создадим в нашем проекте новую директорию и поместим в нее любой файл.
#
# Отлично, теперь давайте напишем код, для открытия браузера и пропишем там путь до нашего нового файла
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
#
# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# g = Service()
#
# driver = webdriver.Chrome(options=options, service=g)
# driver.get('https://www.lambdatest.com/selenium-playground/upload-file-demo')
# driver.maximize_window()
# time.sleep(3)
#
# path_upload = "C:\\путь до файла\\sampleFile.jpeg"
#
# Теперь нам необходимо произвести отправку данного файла, через кнопку "Выбор файла".
# Для этого мы находим локатор для данной кнопки и используем метод send_keys():
#
# click_button = driver.find_element(By.XPATH, "//input[@id='file']")
# click_button.send_keys(path_upload)
#
# Как видите Мы указываем внутри скобок метода send_keys() переменную path_upload, которая содержит не
# только путь до нашего файла, но и название файла + его формат.
#
# Так же, эту запись можно было представить в следующем виде
#
# click_button = driver.find_element(By.XPATH, "//input[@id='file']")
# click_button.send_keys("C:\\путь до файла\\sampleFile.jpeg")
#
# Отлично, вот Мы и научились загружать файлы в Наш браузер!

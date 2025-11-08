import tempfile
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--lang=en')

# 1) Чистый профиль на каждый запуск (надёжнее, чем реальный профиль)
user_data_dir = tempfile.mkdtemp(prefix="selenium-chrome-profile-")
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
chrome_options.add_argument('--no-first-run')
chrome_options.add_argument('--no-default-browser-check')
chrome_options.add_argument('--disable-sync')
chrome_options.add_argument('--incognito')  # инкогнито дополнительно гасит сохранение паролей

# 2) Правильные prefs для паролей и утечек
prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "translate": {"enable": False},
    "intl.accept_languages": "en,en_US",

    # ВАЖНО: корректные ключи
    "credentials_enable_service": False,     # отключает Google Password Manager
    "profile.password_manager_enabled": False,  # не предлагает сохранить
    "password_manager_leak_detection": False    # не проверяет на утечки
}
chrome_options.add_experimental_option('prefs', prefs)

# 3) Флаги отключения соответствующих фич
chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerOnboarding,EnablePasswordsAccountStorage,SafeBrowsingEnhancedProtection,AutofillServerCommunication,PasswordStrengthIndicator")
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

BASE_URL = "https://www.lambdatest.com/selenium-playground/simple-form-demo"
driver.get(BASE_URL)

# ===================== LOCATORS =====================
input_massage_xpath = "//input[@id='user-message']"
btn_get_checked_value_xpath = "//button[@id='showInput']"
message_txt_xpath = "//p[@id='message']"
input_first_value_xpath = "//input[@id='sum1']"
input_second_value_xpath = "//input[@id='sum2']"
get_sum_xpath = "//button[contains(text(), 'Get Sum')]"
result_xpath = "(//p[@class='mt-20'])[2]"
# ===================== STEPS =====================
def input_msg():
    # Нахожу поле ввода сообщений
    input_field = wait.until(EC.presence_of_element_located((By.XPATH, input_massage_xpath)))
    # Очищаю поле ввода сообщений
    input_field.clear()
    # Ввожу сообщение
    msg = "I'm QA and I love Python"
    input_field.send_keys(msg)
    print(f"Message: {msg} - sent")
    return msg # возвращаем сам текст

def push_get_checked(expected_msg: str):
    # Нахожу кнопку отправки сообщения
    btn_el = wait.until(EC.element_to_be_clickable((By.XPATH, btn_get_checked_value_xpath)))
    # Отправляю сообщение
    btn_el.click()

    actual_message_txt = wait.until(EC.visibility_of_element_located((By.XPATH, message_txt_xpath))).text
    assert expected_msg == actual_message_txt, \
        f"Expected {expected_msg}, got {actual_message_txt}"
    print("Expected message = actual message")

def enter_first_value() -> int:
    # Нахожу первое поле ввода
    first_input_field_el = wait.until(EC.presence_of_element_located((By.XPATH, input_first_value_xpath)))
    first_input_field_el.click()
    print("Первое поле ввода, найдено")
    # Ввожу данные в первое поле ввода
    val_1 = 1563
    first_input_field_el.send_keys(str(val_1)) # явно приводим к строке
    print(f"В первое поле ввода введено: {val_1}")
    return val_1

def enter_second_value() -> int:
    # Нахожу второе поле ввода
    second_input_field_el = wait.until(EC.presence_of_element_located((By.XPATH, input_second_value_xpath)))
    second_input_field_el.click()
    print("Второе поле ввода, найдено")
    # Ввожу данные в первое поле ввода
    val_2 = 5624
    second_input_field_el.send_keys(str(val_2)) # явно приводим к строке
    print(f"Во второе поле ввода введено: {val_2}")
    return val_2

def get_sum(expected_sum: int) -> None:
    # Нахожу кнопку Get Sum
    get_sum_el = wait.until(EC.element_to_be_clickable((By.XPATH, get_sum_xpath)))
    get_sum_el.click()
    print("Кнопка Get Sum нажата, сумма рассчитана")

    actual_sum_txt = wait.until(EC.visibility_of_element_located((By.XPATH, result_xpath))).text
    actual_sum_txt = actual_sum_txt.strip()
    print(f"Текст суммы на странице: '{actual_sum_txt}'")

    try:
        actual_sum = int(actual_sum_txt)
    except ValueError:
        raise AssertionError(f"Result '{actual_sum_txt}' не удалось преобразовать в int")
    assert actual_sum == expected_sum, (
        f"Expected sum {expected_sum}, got {actual_sum}"
    )
    print(f"Expected sum: {expected_sum} == actual sum: {actual_sum}")


# ===================== RUN =====================
msg = input_msg() # Сохраняем возвращаемое значение
push_get_checked(msg) # Передаем его в функцию
val_1 = enter_first_value()
val_2 = enter_second_value()
expected_sum = val_1 + val_2
print(f"Ожидаемая сумма (val_1 + val_2): {expected_sum}")
get_sum(expected_sum)
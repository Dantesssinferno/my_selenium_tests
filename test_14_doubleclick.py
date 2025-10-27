import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--guest')
prefs = {
    "translate": {"enable": False},
    "intl.accept_languages": "en,en_US"
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--lang=en')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://demoqa.com/buttons')
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)
action = ActionChains(driver)

# ===================== LOCATORS =====================
bt_double_click_xpath = "//button[@id='doubleClickBtn']"
double_click_txt_xpath = "//p[@id='doubleClickMessage']"
right_click_xpath = "//button[@id='rightClickBtn']"
right_click_txt_xpath = "//p[@id='rightClickMessage']"

# ===================== STEPS =====================
def double_click() -> None:
     double = wait.until(EC.element_to_be_clickable((By.XPATH, bt_double_click_xpath)))
     action.double_click(double).perform() # double_click(double) - помещаем переменную с локатором
     print("Double click: Passed") # perform() - для сохранения результатов

     # проверка двойного нажатия
     double_txt = wait.until(EC.visibility_of_element_located((By.XPATH, double_click_txt_xpath))).text
     assert double_txt == "You have done a double click", f"Ожидал 'Yes', получил '{double_txt}'"
     print("Assert: result == 'You have done a double click' : Passed")

def right_click() -> None:
    right_click = wait.until(EC.element_to_be_clickable((By.XPATH, right_click_xpath)))
    action.context_click(right_click).perform() # context_click(right_click)print - для клика право клавишей
    print("Right click: Passed") # .perform() - для сохранения результатов

    # проверка клика правой клавишей мыши
    right_click = wait.until(EC.visibility_of_element_located((By.XPATH, right_click_txt_xpath))).text
    assert right_click == "You have done a right click", f"Ожидал 'You have done a right click', получил '{right_click}'"
    print("Assert: result == 'You have done a right click' : Passed")


double_click()
right_click()


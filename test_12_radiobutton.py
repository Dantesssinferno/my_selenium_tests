import time
from selenium import webdriver
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
driver.get('https://demoqa.com/radio-button')
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)

# ===================== LOCATORS =====================
rb_yes_xpath = "//label[@for='yesRadio']"
rb_span_result_xpath = "//span[contains(text(), 'Yes')]"

# ===================== STEPS =====================
def click_check_boxes() -> None:
    radiobutton_yes = wait.until(EC.element_to_be_clickable((By.XPATH, rb_yes_xpath)))
    radiobutton_yes.click()
    print("Radiobutton Yes: clicked")

    # проверка результата
    span_txt = wait.until(EC.visibility_of_element_located((By.XPATH, rb_span_result_xpath))).text
    assert span_txt == "Yes", f"Ожидал 'Yes', получил '{span_txt}'"
    print("Assert: result == 'Yes' : Passed")
click_check_boxes()
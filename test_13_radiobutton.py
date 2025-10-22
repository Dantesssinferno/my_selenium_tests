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
driver.get('https://testpages.herokuapp.com/styled/basic-html-form-test.html')
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)

# ===================== LOCATORS =====================
rb_1_xpath = "//input[@value='rd1']"
rb_2_xpath = "//span[contains(text(), 'Yes')]"

# ===================== STEPS =====================
def click_rb() -> None:
    rb_1 = wait.until(EC.element_to_be_clickable((By.XPATH, rb_1_xpath)))
    rb_1.click()
    print("Radiobutton 1: clicked")

click_rb()
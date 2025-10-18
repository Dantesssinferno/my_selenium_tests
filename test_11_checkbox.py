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
check_box_1_xpath = "(//input[@type='checkbox'])[1]"
check_box_2_xpath = "(//input[@type='checkbox'])[2]"
check_box_3_xpath = "(//input[@type='checkbox'])[3]"

# ===================== STEPS =====================
def click_check_boxes(check_box_3_xpath: str) -> None:
    checkboxes = [
        (check_box_1_xpath, 'Checkbox_1'),
        (check_box_2_xpath, 'Checkbox_2'),
        (check_box_3_xpath, 'Checkbox_3')
    ]
    for xpath, name in checkboxes:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        time.sleep(1)
        if element.is_selected():
            print(f"{name}: Clicked ✅")
        else:
            print(f"{name}: ❌ не был выбран")
    check_box_3_el = wait.until(EC.element_to_be_clickable((By.XPATH, check_box_3_xpath))).click()
    print(f"Checkbox_3: Clicked ✅")
click_check_boxes(check_box_3_xpath)

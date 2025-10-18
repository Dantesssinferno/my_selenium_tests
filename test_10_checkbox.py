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
driver.get('https://demoqa.com/elements')
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)

# ===================== LOCATORS =====================
# Меню → Check Box
check_box_elements_menu_xpath = "//li[@id='item-1']"  # XPATH
# Кнопка-стрелка раскрытия Home
toggle_xpath = "//button[@title='Toggle']"            # XPATH
# Чекбокс Home
check_box_home_xpath = "//label[@for='tree-node-home']//span[contains(@class,'rct-checkbox')]"  # XPATH
# Блок выбранных элементов (CSS!)
selected_items_css = "#result span.text-success"      # CSS_SELECTOR

# ===================== HELPERS =====================
def open_check_box_section() -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, check_box_elements_menu_xpath))).click()
    print('Шаг 1.1: открыт раздел Check Box')

def expand_home() -> None:
    wait.until(EC.presence_of_element_located((By.XPATH, toggle_xpath)))
    wait.until(EC.element_to_be_clickable((By.XPATH, toggle_xpath))).click()
    print('Шаг 1.2: найден и нажат toggle_checkbox')

def click_home_checkbox() -> None:
    wait.until(EC.element_to_be_clickable((By.XPATH, check_box_home_xpath))).click()
    print('Шаг 2.1: нажат чекбокс Home')

def assert_selected_has_home() -> None:
    # ВАЖНО: здесь ищем по CSS, значит By.CSS_SELECTOR!
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selected_items_css)))
    selected = [el.text.strip().lower() for el in driver.find_elements(By.CSS_SELECTOR, selected_items_css)]
    print(f"Фактически выбрано: {selected}")
    assert 'home' in selected, f"Ожидал 'home' среди выбранных, получили: {selected}"
    print("Шаг 2.2: Проверка результата: Passed")

# ===================== TEST EXECUTION =====================
open_check_box_section()
expand_home()
click_home_checkbox()
assert_selected_has_home()

time.sleep(2)
driver.quit()
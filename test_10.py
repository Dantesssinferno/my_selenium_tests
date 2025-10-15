import time
from decimal import Decimal, ROUND_HALF_UP

from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===================== BROWSER SETUP =====================

BROWSER = 'chrome'
chrome_options = ChromiumOptions()
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--guest')
prefs = {
    "translate": {"enable": False},
    "intl.accept_languages": "en,en_US"
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--lang=en')
driver = webdriver.Chrome(options=chrome_options)
base_url = 'https://demoqa.com/elements'
driver.get(base_url)
driver.set_window_size(1440, 860)
wait = WebDriverWait(driver, 10)

# ===================== LOCATORS =====================
check_box_elements_menu_xpath = "//li[@id='item-1']"
# Точный локатор чекбокса Home (коробочка слева от надписи Home)
check_box_home_xpath = "//label[@for='tree-node-home']//span[contains(@class,'rct-checkbox')]"
# Все выбранные пункты в блоке результата
selected_items_css = "#result span.text-success"


# ===================== HELPERS =====================
def checkbox(check_box_elements_menu_xpath: str, check_box_home_xpath: str, selected_items_css: str) -> None:
    # Открыть подраздел Check Box
    wait.until(EC.element_to_be_clickable((By.XPATH, check_box_elements_menu_xpath))).click()
    print('Шаг 1.1: найден checkbox: menu > check_box > elements')
    # Клик по чекбоксу Home (выберет Home и всю вложенность)
    wait.until(EC.element_to_be_clickable((By.XPATH, check_box_home_xpath))).click()
    print('Шаг 1.2: найден checkbox: Home')
    # Ждём появления блока результата и читаем выбранные элементы
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selected_items_css)))
    selected = [el.text.strip().lower() for el in driver.find_elements(By.CSS_SELECTOR, selected_items_css)]
    print(f"Фактически выбрано: {selected}")
    # Минимальная проверка: в выбранных есть 'home'
    assert 'home' in selected, f"Ожидал, что 'home' будет среди выбранных, по получили: {selected}"
    print("Шаг 1.3: Проверка результата: Passed")



checkbox(check_box_elements_menu_xpath, check_box_home_xpath, selected_items_css)
time.sleep(3)
driver.quit()

#     print('Шаг 1.3: Клик по Login — OK')
#     # Проверим, что авторизовались (url inventory.html)
#     wait.until(EC.url_contains("inventory.html"))
#     print('Шаг 1.4: Проверка URL inventory — OK')

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ================================================= BROWSER SETUP ======================================================

def create_driver(browser_name: str = "chrome"):
    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--guest')
        prefs = {
            "translate": {"enable": False},
            "intl.accept_languages": "en,en_US"
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--lang=en")
        driver_ = webdriver.Chrome(options=chrome_options)

    elif browser_name == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("browser.translations.enable", False)
        firefox_options.set_preference("intl.accept_languages", "en-US, en")
        # firefox_options.add_argument("-headless")
        firefox_options.add_argument("-width=1440")
        firefox_options.add_argument("-height=860")
        driver_ = webdriver.Firefox(options=firefox_options)

    else:
        raise ValueError("browser_name должен быть 'chrome' или 'firefox'")

    try:
        driver_.set_window_size(1440, 860)
    except Exception:
        pass

    return driver_


BASE_URL = "https://www.saucedemo.com/"

# Тестовые данные
LOGIN_STANDARD_USER = "standard_user"
PASSWORD_UNIVERSAL = "secret_sauce"

FIRST_NAME_VALUE = "Maxim"
LAST_NAME_VALUE = "Starostenko"
POSTAL_CODE_VALUE = "MD-5400"


# ================================================= BASE PAGE ==========================================================

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator: tuple[By, str]) -> None:
        self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.find_element(*locator).click()

    def type_text(self, locator: tuple[By, str], text: str) -> None:
        self.wait.until(EC.visibility_of_element_located(locator))
        el = self.driver.find_element(*locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator: tuple[By, str]) -> str:
        self.wait.until(EC.visibility_of_element_located(locator))
        el = self.driver.find_element(*locator)
        return el.text


# ================================================= LOGIN PAGE =========================================================

class LoginPage(BasePage):
    USERNAME = (By.XPATH, "//input[@name='user-name']")
    PASSWORD = (By.XPATH, "//input[@id='password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")

    def open(self):
        self.driver.get(BASE_URL)

    def login(self, username: str, password: str) -> None:
        self.type_text(self.USERNAME, username)
        print("Шаг: 1: Input Login : success")
        self.type_text(self.PASSWORD, password)
        print("Шаг: 1.1: Input password : success")
        self.click(self.LOGIN_BUTTON)
        print("Шаг: 1.2: Login button clicked : success")
        time.sleep(1)


# ================================================= INVENTORY PAGE =====================================================

class InventoryPage(BasePage):
    # Локаторы каталога через CSS
    INVENTORY_ITEM = (By.CSS_SELECTOR, ".inventory_item")
    INVENTORY_ITEM_NAME_CSS = ".inventory_item_name"
    INVENTORY_ITEM_PRICE_CSS = ".inventory_item_price"
    INVENTORY_ITEM_BUTTON_CSS = "button.btn_inventory"

    CART_LINK = (By.XPATH, "//a[@class='shopping_cart_link']")

    def read_all_products(self) -> list[dict]:
        """
        Считывает все товары на странице каталога и возвращает список словарей:
        {
            "index": 1,
            "title": "...",
            "price": "...",
            "button": <WebElement кнопки Add to cart>
        }
        """
        self.wait.until(EC.presence_of_all_elements_located(self.INVENTORY_ITEM))
        items = self.driver.find_elements(*self.INVENTORY_ITEM)

        products: list[dict] = []
        print("Шаг: 2: Найдены товары в каталоге:")
        for idx, item in enumerate(items, start=1):
            title_el = item.find_element(By.CSS_SELECTOR, self.INVENTORY_ITEM_NAME_CSS)
            price_el = item.find_element(By.CSS_SELECTOR, self.INVENTORY_ITEM_PRICE_CSS)
            button_el = item.find_element(By.CSS_SELECTOR, self.INVENTORY_ITEM_BUTTON_CSS)

            title_text = title_el.text
            price_text = price_el.text

            products.append(
                {
                    "index": idx,
                    "title": title_text,
                    "price": price_text,
                    "button": button_el,
                }
            )
            print(f"  {idx}. {title_text} - {price_text}")

        print(f"Всего товаров: {len(products)}")
        return products

    def select_product_by_button(self, button_element) -> None:
        # Ждём кликабельности элемента и кликаем
        self.wait.until(EC.element_to_be_clickable(button_element))
        button_element.click()
        print("Шаг: 3: Selected product: Passed")

    def open_cart(self) -> None:
        self.click(self.CART_LINK)
        print("Шаг: 4: Enter cart: Passed")


# ================================================= CART PAGE ==========================================================

class CartPage(BasePage):
    CART_PRODUCT_NAME = (By.XPATH, "//div[@class='inventory_item_name'][1]")
    CART_PRODUCT_PRICE = (By.XPATH, "//div[@class='inventory_item_price'][1]")
    CART_CHECKOUT_BUTTON = (By.XPATH, "//button[@id='checkout']")

    def get_first_item_info(self) -> tuple[str, str]:
        name = self.get_text(self.CART_PRODUCT_NAME)
        print(f"Шаг: 5: {name}")
        price = self.get_text(self.CART_PRODUCT_PRICE)
        print(f"Шаг: 6: {price}")
        time.sleep(1)
        return name, price

    def go_to_checkout(self) -> None:
        self.click(self.CART_CHECKOUT_BUTTON)
        print("Шаг: 7: Checkout button clicked : success")
        time.sleep(1)


# ================================================= CHECKOUT PAGE ======================================================

class CheckoutPage(BasePage):
    # Step One
    FIRST_NAME = (By.XPATH, "//input[@id='first-name']")
    LAST_NAME = (By.XPATH, "//input[@id='last-name']")
    POSTAL_CODE = (By.XPATH, "//input[@id='postal-code']")
    CONTINUE_BUTTON = (By.XPATH, "//input[@id='continue']")

    # Step Two (Overview)
    OVERVIEW_TITLE = (By.XPATH, "//div[@data-test='inventory-item-name']")
    OVERVIEW_PRICE = (By.XPATH, "//div[@data-test='inventory-item-price']")
    ITEM_TOTAL = (By.XPATH, "//div[@class='summary_subtotal_label']")

    # Finish и Complete
    FINISH_BUTTON = (By.XPATH, "//button[@id='finish']")
    FINISH_TEXT = (By.XPATH, "//h2[@data-test='complete-header']")
    BACK_HOME_BUTTON = (By.XPATH, "//button[@id='back-to-products']")

    def fill_user_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.type_text(self.FIRST_NAME, first_name)
        print("Шаг: 8.1: input first name: success")
        time.sleep(1)

        self.type_text(self.LAST_NAME, last_name)
        print("Шаг: 8.2: input last name: success")
        time.sleep(1)

        self.type_text(self.POSTAL_CODE, postal_code)
        print("Шаг: 8.3: input postal code: success")
        time.sleep(1)

        self.click(self.CONTINUE_BUTTON)
        print("Шаг: 8.4: Continue button clicked: success")
        self.wait.until(EC.url_contains("checkout-step-two.html"))

    def get_overview_item_info(self) -> tuple[str, str]:
        title = self.get_text(self.OVERVIEW_TITLE)
        print(f"Шаг: 9.1: {title}")
        price = self.get_text(self.OVERVIEW_PRICE)
        print(f"Шаг: 9.2: {price}")
        return title, price

    def get_item_total(self) -> str:
        total_text = self.get_text(self.ITEM_TOTAL)
        print(f"Шаг: 10: {total_text}")
        return total_text

    def finish_checkout(self) -> str:
        self.click(self.FINISH_BUTTON)
        print("Шаг: 11: Finish Checkout button clicked : success")
        time.sleep(1)

        finish_text = self.get_text(self.FINISH_TEXT)
        print(f"Шаг: 11.1: Finish text {finish_text}")
        time.sleep(1)
        return finish_text

    def back_home(self) -> str:
        self.click(self.BACK_HOME_BUTTON)
        print("Шаг: 12: Back home button clicked : success")
        time.sleep(1)

        self.wait.until(EC.url_contains("inventory.html"))
        catalog_url = self.driver.current_url
        print(f"Шаг: 12.1: Current URL is: {catalog_url}")
        return catalog_url


# ================================================= ВСПОМОГАТЕЛЬНАЯ ЛОГИКА ============================================

def ask_user_choice(products: list[dict]) -> dict:
    """
    Спрашивает у пользователя номер товара, пока не будет введён корректный номер.
    Возвращает словарь с выбранным товаром из списка products.
    """
    max_index = len(products)
    while True:
        choice_str = input(f"Введите номер товара, который хотите заказать (1-{max_index}): ").strip()

        if not choice_str.isdigit():
            print("Нужно ввести число. Попробуйте ещё раз.")
            continue

        choice = int(choice_str)
        if 1 <= choice <= max_index:
            chosen_product = products[choice - 1]
            print(
                f"Вы выбрали товар №{choice}: "
                f"{chosen_product['title']} - {chosen_product['price']}"
            )
            return chosen_product
        else:
            print(f"Неверный номер. Введите число от 1 до {max_index}.")


# ==================================================== TEST FLOW =======================================================

def run_test() -> None:
    driver = create_driver("chrome")
    try:
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(LOGIN_STANDARD_USER, PASSWORD_UNIVERSAL)

        inventory_page = InventoryPage(driver)
        products = inventory_page.read_all_products()
        chosen = ask_user_choice(products)

        name_catalog = chosen["title"]
        price_catalog = chosen["price"]

        inventory_page.select_product_by_button(chosen["button"])
        inventory_page.open_cart()

        cart_page = CartPage(driver)
        name_cart, price_cart = cart_page.get_first_item_info()

        assert name_catalog.strip() == name_cart.strip(), \
            f"Имя товара не совпало: '{name_catalog}' vs '{name_cart}'"
        print("Шаг: 6.1: Name catalog = name cart: Passed")

        assert price_catalog.strip() == price_cart.strip(), \
            f"Цена товара не совпала: '{price_catalog}' vs '{price_cart}'"
        print("Шаг: 6.2: Price catalog = price cart: Passed")

        cart_page.go_to_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_user_info(FIRST_NAME_VALUE, LAST_NAME_VALUE, POSTAL_CODE_VALUE)

        overview_title, overview_price = checkout_page.get_overview_item_info()
        total_sum_text = checkout_page.get_item_total()

        assert name_cart.strip() == overview_title.strip(), \
            f"Имя товара не совпало: '{name_cart}' vs '{overview_title}'"
        print("Шаг: 10.1: Name cart = name checkout overview: Passed")

        assert price_cart.strip() == overview_price.strip(), \
            f"Цена товара не совпала: '{price_cart}' vs '{overview_price}'"
        print("Шаг: 10.2: Price cart = price checkout overview: Passed")

        finish_text = checkout_page.finish_checkout()
        back_home_url = checkout_page.back_home()

        print("Тест завершён успешно.")
        print("Финальное сообщение:", finish_text)
        print("URL каталога после Back home:", back_home_url)
        print("Item total:", total_sum_text)

    finally:
        # Если хочешь оставлять окно открытым — можно закомментировать
        driver.quit()


# ======================================================= ENTRYPOINT ===================================================

if __name__ == "__main__":
    run_test()

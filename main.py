from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager



options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

options.add_argument("--guest")

driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

base_url = 'https://www.saucedemo.com/'

driver.get(base_url)

driver.maximize_window()
driver.get("https://www.saucedemo.com/")
driver.maximize_window()

from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))




base_url = 'https://www.saucedemo.com/'

driver.get(base_url)

driver.maximize_window()

from selenium import webdriver




driver = webdriver.Chrome()

driver.get('https://www.saucedemo.com/')

driver.maximize_window()

from selenium import webdriver




driver = webdriver.Firefox()

driver.get("https://www.saucedemo.com/")

driver.maximize_window()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--guest")
g = Service()
driver = webdriver.Chrome(options=options, service=g)
base_url = 'https://www.saucedemo.com/'
driver.get(base_url)
driver.maximize_window()
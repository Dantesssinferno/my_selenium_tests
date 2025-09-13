import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService


# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# g = Service()
#
# driver = webdriver.Chrome(options=options, service=g)

options = webdriver.FirefoxOptions()
f = FirefoxService()
driver = webdriver.Firefox(options=options, service=f)
base_url = 'http://www.saucedemo.com/'
driver.get(base_url)
driver.maximize_window()

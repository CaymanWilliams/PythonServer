import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

#driver initialization
def initializeDriver():
    #dc = webdriver.DesiredCapabilities.HTMLUNIT

    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    #option.add_argument("--headless")
    option.add_argument('log-level=3')

    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    global driver
    global wait
    #driver = webdriver.Remote("http://localhost:4444/wd/hub", dc)
    driver = webdriver.Chrome(options = option, executable_path = "./env/chromedriver.exe")
    wait = WebDriverWait(driver, 10)

#logs into offerup
def offerUpLogin(user, passkey):
    driver.get("https://offerup.com")
    login = driver.find_element_by_id("db-desktop-login")
    login.click()
    email = wait.until(EC.presence_of_element_located((By.ID, "db-email-input")))
    email.clear()
    email.send_keys(user)
    password = driver.find_element_by_id("db-password-input")
    password.clear()
    password.send_keys(passkey)
    login = driver.find_element_by_id("db-submit-btn")
    login.click()
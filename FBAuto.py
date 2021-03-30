import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

#model class for a facebook item
class FBItem:
    def __init__(self, name, price, cat, condition, location, description, photos):
        self.name = name
        self.price = price
        self.cat = cat
        self.condition = condition
        self.location = location
        self.description = description
        self.photos = photos

#initializes the selenium driver
def initializeDriver():
    #dc = webdriver.DesiredCapabilities.HTMLUNIT

    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_argument("--headless")
    option.add_argument('log-level=3')

    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    global driver
    global wait
    #driver = webdriver.Remote("http://localhost:4444/wd/hub", dc)
    driver = webdriver.Chrome(options = option, executable_path = "./env/chromedriver.exe")
    wait = WebDriverWait(driver, 10)

#defines a clicking function (more robust than a simple click)
def clickWait(element):
    error = True
    t_end = time.time() + 10
    while time.time() < t_end:
        try: 
            element.click()
            time.sleep(.5)
        except:
            error = False
            break
    if error == True:
        raise Exception

#Logs into facebook using the specified details
def FacebookLogin(user, passkey):
    driver.get("https://facebook.com/marketplace")
    username = driver.find_element_by_id("email")
    username.clear()
    username.send_keys(user)
    password = driver.find_element_by_id("pass")
    password.clear()
    password.send_keys(passkey)
    login = driver.find_element_by_xpath('//*[@data-testid="royal_login_button"]')
    login.click()
    wait.until(EC.staleness_of(login))

#navigates to the marketplace tab
def marketplaceNav():
    sellSomething = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Sell Something')]")))
    sellSomething.click()

#posts an item
def itemPost(toSell, user, passkey):
    initializeDriver()
    FacebookLogin(user, passkey)
    marketplaceNav()

    # 1) What are you selling? 2) Price 3) Category (Dropdown) 3.5) Condition 4) Location 5) Description 6) Photos(10) 7) Select Groups
    itemForSale = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Item for Sale')]")))
    itemForSale.click()
    wait.until(EC.staleness_of(itemForSale))

    whatSell = driver.find_element_by_xpath("//*[@placeholder = 'What are you selling?']")
    whatSell.send_keys(toSell.name)

    price = driver.find_element_by_xpath("//*[@placeholder = 'Price']")
    price.send_keys(toSell.price)

    category = driver.find_element_by_xpath("//*[@placeholder = 'Select a Category'][@type = 'text']")
    category.send_keys(toSell.cat)
    category.send_keys(Keys.DOWN)
    category.send_keys(Keys.ENTER)

    condition = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@placeholder = 'Select condition'][@type = 'text']")))
    condition.send_keys(toSell.condition)
    condition.send_keys(Keys.DOWN)
    condition.send_keys(Keys.ENTER)

    description = driver.find_element_by_xpath("//*[@aria-label = 'Describe your item (optional)']")
    description.send_keys(toSell.description)

    photos = driver.find_element_by_xpath("//*[@title = 'Choose a file to upload']")
    photos.send_keys(toSell.photos)

    nextButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
    nextButton.click()

    oldurl = driver.current_url
    publish = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Publish']]")))
    publish.click()

    while driver.current_url == oldurl:
        time.sleep(.5)

    driver.close()

#posts a vehicle
def vehiclePost():
    initializeDriver()
    FacebookLogin()
    marketplaceNav()
    
    # 1) Vehicle type (dropdown) 2) Year (dropdown) 3) Make (dropdown?) 4) Model (dropdown?) 5) Price 6) Location 7) Description 8) Photos(20) ...
    vehicleForSale = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Vehicle for Sale')]")))
    vehicleForSale.click()
    wait.until(EC.staleness_of(vehicleForSale))

#posts a real estate property
def homePost():
    # 1) Sale/Rent? 2) Apartment/House/Room/Townhouse 3) Beds 4) Bath 5) Address (private?) 6) Description Optional: Square Feet, Laundry, Parking, Air Conditioning, Heating type
    homeForSell = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Home for Sale or Rent')]")))
    homeForSell.click()
    wait.until(EC.staleness_of(homeForSell))
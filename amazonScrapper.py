
####### IMPORTS ########
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

######## TYPES ########
type Product = dict["title": str, "price": float, "discount": int]

######## CONSTANTS ########
URL = "https://www.amazon.ca/deals"

######## METHODS ########

def fetch_products() -> list[Product]:
    products: list[Product] = []

######## MAIN ########
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening a window
options.add_argumentq("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)

time.sleep(3) # Wait for JS to load
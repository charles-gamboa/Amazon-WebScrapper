
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

def fetch_products(driver: webdriver.Chrome) -> list[Product]:
    ''' 
    Fetches products from the Amazon deals page using the provided WebDriver. Returns a list of products with their title, price, and discount.
    '''
    products: list[Product] = [] # List of products

    # Select all product cards on the page
    product_cards = driver.find_elements(By.CSS_SELECTOR, ".a-color-base.a-spacing-mini.a-link-normal.a-text-normal")
    #last_count = len(product_cards)

    # Scroll down the page until no new products are found
    scroll_height = 0
    max_scroll_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        
        driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", 0, scroll_height)

        time.sleep(2) # Wait for JS to load
        
        product_cards = driver.find_elements(By.CSS_SELECTOR, ".a-color-base.a-spacing-mini.a-link-normal.a-text-normal") # Re-select all product cards
        #new_count = len(product_cards)

        if scroll_height >= max_scroll_height:
            break
        
        scroll_height += 1000
        #last_count = new_count

    # Select all public data from each product card
    for product_card in product_cards:
        title_element = product_card.find_element(By.CSS_SELECTOR, ".a-truncate-cut")
        price_whole_element = product_card.find_element(By.CSS_SELECTOR, ".a-price-whole")
        price_fraction_element = product_card.find_element(By.CSS_SELECTOR, ".a-price-fraction")
        discount_element = product_card.find_element(By.CSS_SELECTOR, ".style_filledRoundedBadgeLabel__Vo").find_element(By.CSS_SELECTOR, ".a-size-mini")

        title = title_element.text
        price = float(price_whole_element.text.replace("$", "").replace(",", "") + "." + price_fraction_element.text)
        discount = int(discount_element.text[0:2])

        products.append({"title": title, "price": price, "discount": discount})

    return products

######## MAIN ########
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Run without opening a window
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)

time.sleep(1) # Wait for JS to load

products = fetch_products(driver) # Fetch products from the Amazon url page

print(products)

driver.quit() # Exit driver

####### IMPORTS ########
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, random, json

######## TYPES ########
type Product = dict["title": str, "price": float, "discount": int]

######## CONSTANTS ########
URL = "https://www.amazon.ca/deals"

######## METHODS ########

def fetch_products(driver: webdriver.Chrome) -> list[Product]:
    ''' 
    Fetches products from the Amazon deals page using the provided WebDriver. Returns a list of products with their title, price, and discount.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the Amazon page.
    Returns:
        list[Product]: A list of products, where each product is represented as a dictionary containing its title, price, and discount.
    '''
    products: list[Product] = [] # List of products

    # Select all product cards on the page
    product_cards: list[webdriver.Chrome.WebElement] = []
    last_count = len(product_cards)

    # Scroll down the page until no new products are found
    scroll_delay = 2
    scroll_step = 0

    while True:
        driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", 0, scroll_step)
        
        time.sleep(scroll_delay + random.random() * 0.5)
        
        product_cards = driver.find_elements(By.CSS_SELECTOR, ".a-color-base.a-spacing-mini.a-link-normal.a-text-normal") # Select all product cards

        new_count = len(product_cards)

        # Re-try once more
        if new_count <= last_count:
            last_count = new_count
            scroll_step += 500 + random.random() * 500

            driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", 0, scroll_step)
            
            time.sleep(scroll_delay + random.random() * 0.5)

            product_cards = driver.find_elements(By.CSS_SELECTOR, ".a-color-base.a-spacing-mini.a-link-normal.a-text-normal")
            new_count = len(product_cards)

            if new_count <= last_count:
                break

        last_count = new_count
        scroll_step += 1000 + random.random() * 500

    # Select all public data from each product card
    for product_card in product_cards:
        title_element = product_card.find_element(By.CSS_SELECTOR, ".a-truncate-cut")
        price_whole_element = product_card.find_element(By.CSS_SELECTOR, ".a-price-whole")
        price_fraction_element = product_card.find_element(By.CSS_SELECTOR, ".a-price-fraction")
        discount_element = driver.find_element(By.XPATH, "//span[contains(text(), 'off')]")
    
        title = title_element.text
        price = float(price_whole_element.text.replace("$", "").replace(",", "") + "." + price_fraction_element.text)
        discount = int(discount_element.text[0:2])

        products.append({"title": title, "price": price, "discount": discount})

    return products

######## MAIN ########
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening a window
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)

time.sleep(1) # Wait for JS to load

products = fetch_products(driver) # Fetch products from the Amazon url page

driver.quit() # Exit driver

with open("amazonDeals.json", "w") as f:
    json.dump(products, f, indent=4) # Save products to a JSON file

####### IMPORTS ########
import requests, time, random
from bs4 import BeautifulSoup

######## CONSTANTS ########

ATTEMPTS_COUNT = 5 # Number of attempts to fetch the page
HEADERS = { # Realistic headers to mimic a browser request
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

######### METHODS ########

def fetch(url: str, attempts_count: int = ATTEMPTS_COUNT, timeout: int = 10) -> str | None:
    '''
    Fetches the HTML content of a given URL with retries and timeout.
    Args:
        url (str): The URL to fetch.
        attempts_count (int, optional): The number of attempts to make. Defaults to ATTEMPTS_COUNT.
        timeout (int, optional): The timeout for each request in seconds. Defaults to 10.

    Returns:
        str | None: The HTML content of the page if successful, otherwise None.
    '''

    for attempt in range(attempts_count):  # Retry up to 5 times
        response = requests.get(url, headers=HEADERS, timeout=timeout)

        # Make sure response is OK and does not contain a captcha
        if response.status_code == 200 and "captcha" not in response.text.lower():
            return response.text
        time.sleep(random.uniform(1, 3))  # Random delay between attempts
    return None

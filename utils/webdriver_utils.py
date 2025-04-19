from selenium.webdriver.chrome.options import Options as ChromeOptions # type: ignore
from selenium.webdriver.firefox.options import Options as FirefoxOptions # type: ignore
from dotenv import load_dotenv # type: ignore
import os

def get_chrome_options():
    load_dotenv()

    options = ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("window-size=1400x900")
    if os.getenv('APP_ENV') == 'production':
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
    return options

def get_firefox_options():
    load_dotenv()

    options = FirefoxOptions()
    options.add_argument("start-maximized")
    options.add_argument("window-size=1400x900")
    if os.getenv('APP_ENV') == 'production':
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
    return options

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import APP_ENV

def get_chrome_options():
    options = ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("window-size=1400x900")
    if APP_ENV == 'production':
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
    return options

def get_firefox_options():
    options = FirefoxOptions()
    options.add_argument("--width=1400")
    options.add_argument("--height=900")

    if APP_ENV == 'production':
        options.add_argument("--headless")
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.set_preference("media.headless", True)
        options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")
        options.set_preference("dom.ipc.plugins.enabled", "false")

    return options

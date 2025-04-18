from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from database.database import Database
import time

def handler(keyword):
    options = Options()
    # options.add_argument("--headless")  # Si quieres ocultarlo
    db = Database()
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.computrabajo.com.co/trabajo-de-{keyword}?pubdate=7")

    time.sleep(3)  # Dale tiempo a que cargue

    offers = driver.find_elements(By.CLASS_NAME, "box_offer")

    for offer in offers:
        title_element = offer.find_element(By.CLASS_NAME, "js-o-link")
        title = title_element.text
        link = title_element.get_attribute("href")
        db.execute_query("INSERT INTO jobs (title, url) VALUES (?, ?)", (title, link))
        print(f"{title} 👉 {link}")

    driver.quit()

from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
from database.database import Database
import time
import json
from config import EXCLUDE, DAYS, BROWSER
from dotenv import load_dotenv # type: ignore
import os
from utils.webdriver_utils import get_chrome_options, get_firefox_options
from utils.utils import setup_logger

load_dotenv()

isLoggedIn = False

logger = setup_logger(__name__)


def handler(keywords):
    notification_validated = False
    if BROWSER.upper() == 'FIREFOX':
        options = get_firefox_options()
        driver = webdriver.Firefox(options=options)
    else:
        options = get_chrome_options()
        driver = webdriver.Chrome(options=options)

    db = Database()

    driver.get("https://co.computrabajo.com/")
    load_cookies(driver, 'computrabajo', ['cookieconsent_status', 'ct_consent', 'SLO_GWPT_Show_Hide_tmp'])
    driver.set_window_size(1400, 900)

    
    try:
        for keyword in keywords:
            print(f"\n🔍 Buscando ofertas para: {keyword}\n")

            pagination = 1
            while True:
                driver.get(f"https://co.computrabajo.com/trabajo-de-{keyword}?pubdate={DAYS}&p={pagination}")
                time.sleep(3)
                
                if not notification_validated:
                    try:
                        # Espera a que aparezca el popup
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.ID, "pop-up-webpush-sub"))
                        )
                        # Cierra popup dando clic en "Ahora no"
                        close_button = driver.find_element(By.XPATH, "//button[contains(text(),'Ahora no')]")
                        close_button.click()
                        print("✅ Popup cerrado.")
                        notification_validated = True
                        
                    except:
                        print("✅ No apareció el popup.")
                        notification_validated = True

                try:
                    offers = WebDriverWait(driver, 8).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "box_offer"))
                    )
                except TimeoutException:
                    print("⏰ No se pudieron cargar las ofertas, saliendo de esta búsqueda...")
                    break

                if not offers:
                    print("✅ Sin más ofertas en esta página.")
                    break

                filtered_offers = [o for o in offers if not any(e in o.text for e in EXCLUDE)]

                for offer in filtered_offers:
                    try:
                        title_element = offer.find_element(By.CLASS_NAME, "js-o-link")
                        title = title_element.text
                        link = title_element.get_attribute("href").strip()
                        try:
                            company = offer.find_element(By.CLASS_NAME, "t_ellipsis").text
                        except:
                            company = "Anonimo"
                        job_id = offer.get_attribute("data-id")
                        salary = contract_type = schedule = modality = "No especificado"
                        
                        offer.click()
                        time.sleep(3)
                        try:
                            description = driver.find_element(By.CLASS_NAME, "t_word_wrap").text
                            details = driver.find_elements(By.CSS_SELECTOR, ".mbB p")

                            for detail in details:
                                icons = detail.find_elements(By.TAG_NAME, "span")
                                if not icons:
                                    continue
                                
                                icon = icons[0].get_attribute("class")

                                if "i_money" in icon:
                                    salary = detail.text.strip()
                                elif "i_find" in icon:
                                    contract_type = detail.text.strip()
                                elif "i_clock" in icon:
                                    schedule = detail.text.strip()
                                elif "i_home" in icon:
                                    modality = detail.text.strip()

                        except Exception as e:
                            print(f"⚠️ Error obteniendo detalles: {e}")
                            description = "Descripción no disponible"

                        # Guardar en la base de datos
                        db.execute_query("""
                            INSERT OR IGNORE INTO jobs 
                            (title, url, company, job_id, salary, contract_type, schedule, modality, description, status, created_at) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', datetime('now', 'localtime'))
                        """, (title, link, company, job_id, salary, contract_type, schedule, modality, description))

                        print(f"{title} 👉 {link}")

                    except Exception as e:
                        print(f"❌ Error procesando oferta: {e}")

                pagination += 1

    except Exception as e:
        logger.error(f"Error en el scraping: {e}")

    finally:
        driver.quit()  # Cerrar el driver una vez que todo termine

    print("✅ Scraping finalizado.")



def load_cookies(driver, context, include_only=[]):
    try:
        file_path="cookies.json"
        with open(file_path, "r") as file:
            cookies = json.load(file)
        for cookie in cookies[context]:
            if include_only and cookie['name'] not in include_only:
                continue
            if cookie['name'] == 'uca':
                cookie['value'] = os.getenv('COOKIE_UCA')
            driver.add_cookie(cookie)
        print("Cookies cargadas.")
    except FileNotFoundError:
        logger.error("No se encontraron cookies.")

def bot_apply(url, job_id):
    if BROWSER.upper() == 'FIREFOX':
        options = get_firefox_options()
        driver = webdriver.Firefox(options=options)
    else:
        options = get_chrome_options()
        driver = webdriver.Chrome(options=options)

    db = Database()
    driver.get("https://co.computrabajo.com/")

    load_cookies(driver, 'computrabajo')

    driver.get(url)

    time.sleep(3)

    try:

        apply_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.b_primary.big.w100"))
        )
        apply_button.click()

        time.sleep(3)


        success_locator = (By.XPATH, "//p[contains(text(), 'Te aplicaste correctamente')]")
        already_applied_locator = (By.XPATH, "//p[contains(text(), 'Ya aplicaste a esta oferta')]")

        try:
            # Esperar uno de los dos mensajes
            message = WebDriverWait(driver, 4).until(
                EC.any_of(
                    EC.presence_of_element_located(success_locator),
                    EC.presence_of_element_located(already_applied_locator)
                )
            )
            if message.is_displayed():
                db.execute_query("UPDATE jobs SET status = 'applied' WHERE job_id = ?", (job_id,))
                return ["✅ Aplicado", 1]
            else:
                db.execute_query("UPDATE jobs SET status = 'failed' WHERE job_id = ?", (job_id,))
                return ["⚠️ No se pudo confirmar la aplicación. Revísalo manualmente.", 0]

        except TimeoutException:
            db.execute_query("UPDATE jobs SET status = 'failed' WHERE job_id = ?", (job_id,))
            return ["⚠️ No se pudo confirmar la aplicación. Revísalo manualmente.", 0]

    except TimeoutException:
        db.execute_query("UPDATE jobs SET status = 'failed' WHERE job_id = ?", (job_id,))
        return ["⚠️ No se pudo encontrar el botón de aplicación.", 0]

    finally:
        driver.quit()

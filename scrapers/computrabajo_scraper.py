from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import TimeoutException # type: ignore
from core.interfaces import IScraper
from database.database import Database
import time
from config import EXCLUDE, BROWSER, COMPUTRABAJO_URL
from utils.webdriver_utils import get_chrome_options, get_firefox_options
from utils.utils import setup_logger, salary_to_int
from services.computrabajo_service import ComputrabajoService

class ComputrabajoScraper(IScraper):
    def __init__(self):
        self.db = Database()
        self.logger = setup_logger(__name__)
        self.url = COMPUTRABAJO_URL
        

    def scrape(self, keywords):
        notification_validated = False
        if BROWSER.upper() == 'FIREFOX':
            options = get_firefox_options()
            driver = webdriver.Firefox(options=options)
        else:
            options = get_chrome_options()
            driver = webdriver.Chrome(options=options)

        driver.get(self.url)

        compputrabajo_service = ComputrabajoService()
        compputrabajo_service.load_cookies(driver, ['cookieconsent_status', 'ct_consent', 'SLO_GWPT_Show_Hide_tmp'])
        
        driver.set_window_size(1400, 900)
        
        try:
            existing_jobs = self.db.execute_query("SELECT job_id FROM jobs").fetchall()
            existing_job_ids = set(job[0] for job in existing_jobs)
            exclude_lower = [e.lower() for e in EXCLUDE]

            for keyword in keywords:
                print(f"\n🔍 Buscando ofertas para: {keyword}\n")

                pagination = 1
                while True:
                    driver.get(f"{self.url}trabajo-de-{keyword}?p={pagination}")

                    if not notification_validated:
                        try:
                            # Espera a que aparezca el popup
                            WebDriverWait(driver, 10).until(
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
                        offers_elements = WebDriverWait(driver, 8).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "box_offer"))
                        )
                        offers = [o for o in offers_elements if o.get_attribute("data-id") not in existing_job_ids]
                    except TimeoutException:
                        print("⏰ No se pudieron cargar las ofertas, saliendo de esta búsqueda...")
                        break

                    if not offers:
                        print("✅ Sin más ofertas en esta página.")
                        break


                    filtered_offers = [
                        o for o in offers 
                        if not any(e in o.text.lower() for e in exclude_lower)
                        and ("hace" in o.text.lower() or "ayer" in o.text.lower())
                    ]

                    for offer in filtered_offers:
                        try:
                            title_element = offer.find_element(By.CLASS_NAME, "js-o-link")
                            title = title_element.text
                            link = title_element.get_attribute("href").strip()
                            try:
                                company = offer.find_element(By.CLASS_NAME, "t_ellipsis").text
                            except:
                                company = None

                            job_id = offer.get_attribute("data-id")
                            salary = contract_type = schedule = modality = location = None
                            
                            try:
                                location_elements = offer.find_elements(By.CSS_SELECTOR, "p.fs16.fc_base.mt5 span.mr10")
                                location = location_elements[1].text if len(location_elements) > 1 else None
                            except:
                                location = None
                            
                            offer.click()
                            time.sleep(1.5)
                            try:
                                description = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, "t_word_wrap"))
                                ).text
                                details = driver.find_elements(By.CSS_SELECTOR, ".mbB p")

                                for detail in details:
                                    icons = detail.find_elements(By.TAG_NAME, "span")
                                    if not icons:
                                        continue
                                    
                                    icon = icons[0].get_attribute("class")
                                    
                                    if "i_money" in icon:
                                        salary = detail.text.strip() or None
                                    elif "i_find" in icon:
                                        contract_type = detail.text.strip() or None
                                    elif "i_clock" in icon:
                                        schedule = detail.text.strip() or None
                                    elif "i_home" in icon:
                                        modality = detail.text.strip() or None

                            except Exception as e:
                                print(f"⚠️ Error obteniendo detalles: {e}")
                                description = None

                            salary_int = salary_to_int(salary) if salary else 0
                        
                            compputrabajo_service.create_job(title, link, company, job_id, salary, contract_type, schedule, modality, description, location, status = 'pending', salary_int = salary_int)
                                        
                            print(f"✅ Oferta guardada: {title}")
                        except Exception as e:
                            print("❌ Error procesando oferta: Revisa los detalles en los loggers.")
                            self.logger.error(f"Error procesando oferta: {e}")

                    pagination += 1

        except Exception as e:
            print("Error en el scraping: Revisa los detalles en los loggers.")
            self.logger.error(f"Error en el scraping: {e}")

        finally:
            driver.quit()

        print("✅ Scraping finalizado.")

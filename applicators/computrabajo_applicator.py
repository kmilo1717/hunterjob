from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from core.interfaces import IApplicator
from database.database import Database
from utils.webdriver_utils import get_chrome_options, get_firefox_options
from utils.utils import setup_logger
from services.computrabajo_service import ComputrabajoService
from config import BROWSER, COMPUTRABAJO_URL


class ComputrabajoApplicator(IApplicator):
    def __init__(self, job_id):
        self.logger = setup_logger(__name__)
        self.url = COMPUTRABAJO_URL
        self.job_id = job_id

    def apply(self, apply_url):
        if BROWSER.upper() == 'FIREFOX':
            options = get_firefox_options()
            driver = webdriver.Firefox(options=options)
        else:
            options = get_chrome_options()
            driver = webdriver.Chrome(options=options)

        db = Database()
        driver.get(self.url)

        compputrabajo_service = ComputrabajoService()
        compputrabajo_service.load_cookies(driver)
        driver.set_window_size(1400, 900)

        driver.get(apply_url)


        try:

            apply_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.b_primary.big.w100"))
            )
            apply_button.click()

            success_locator = (By.XPATH, "//p[contains(text(), 'Te aplicaste correctamente')]")
            already_applied_locator = (By.XPATH, "//p[contains(text(), 'Ya aplicaste a esta oferta')]")

            try:
                # Esperar uno de los dos mensajes
                message = WebDriverWait(driver, 3).until(
                    EC.any_of(
                        EC.presence_of_element_located(success_locator),
                        EC.presence_of_element_located(already_applied_locator)
                    )
                )
                if message.is_displayed():
                    db.update_one("jobs", "UPDATE jobs SET status = 'applied' WHERE id = ?", {"id": self.job_id, "status": "applied"})
                    return ["✅ Aplicado", 1]
                else:
                    db.update_one("jobs", "UPDATE jobs SET status = 'failed' WHERE id = ?", {"id": self.job_id, "status": "failed"})
                    return ["⚠️ No se pudo confirmar la aplicación. Revísalo manualmente.", 0]

            except TimeoutException:
                db.update_one("jobs", "UPDATE jobs SET status = 'failed' WHERE id = ?", {"id": self.job_id, "status": "failed"})
                return ["⚠️ No se pudo confirmar la aplicación. Revísalo manualmente.", 0]

        except TimeoutException:
            db.update_one("jobs", "UPDATE jobs SET status = 'failed' WHERE id = ?", {"id": self.job_id, "status": "failed"})
            return ["⚠️ No se pudo encontrar el botón de aplicación.", 0]

        finally:
            driver.quit()
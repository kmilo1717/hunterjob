from dotenv import load_dotenv  # Importar load_dotenv para cargar variables de entorno
import os

load_dotenv()

# Variables de configuración
BROWSER = 'Chrome'  # Puede ser 'Chrome', 'Firefox'
EXCLUDE = ['BairesDev LLC']
INTEREST_JOBS = ['php', 'laravel', 'frontend', 'backend']
DAYS = '1'

# Variables de entorno cargadas desde el archivo .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_NAME = os.getenv('DB_NAME')
COOKIE_UCA = os.getenv('COOKIE_UCA')
APP_ENV = os.getenv('APP_ENV')

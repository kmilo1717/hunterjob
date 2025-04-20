from dotenv import load_dotenv  # Importar load_dotenv para cargar variables de entorno
import os

load_dotenv()

# Variables de configuración
BROWSER = 'Chrome'  # Puede ser 'Chrome', 'Firefox'
INTEREST_JOBS = ['php', 'laravel']
FILTERS = {
    'MIN_SALARY': 3000000,
    'MODALITY': ['Remoto', 'Presencial y remoto'],
}
EXCLUDE = [
    'vendedor',
]
HIGHLIGHTS = ['remoto']

# Variables de entorno cargadas desde el archivo .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_NAME = os.getenv('DB_NAME')
COOKIE_UCA = os.getenv('COOKIE_UCA')
APP_ENV = os.getenv('APP_ENV')

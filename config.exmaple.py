from dotenv import load_dotenv  # Importar load_dotenv para cargar variables de entorno
import os

load_dotenv()

# Variables de configuración
BROWSER = 'Chrome'  # Puede ser 'Chrome', 'Firefox'
INTEREST_JOBS = ['php', 'laravel']
MODALITIES = {
    'Hybrid': 4000000,
    'Remote': 2000000,
    'Onsite': 5000000
}
SCHEDULES = ['Tiempo Parcial', 'Tiempo Completo', 'Por Horas']
EXCLUDE = [
    'vendedor',
]
HIGHLIGHTS = ['remoto']

# Variables de configuración
COMPUTRABAJO_URL = 'https://co.computrabajo.com/'

# Variables de entorno cargadas desde el archivo .env
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
DB_NAME = os.getenv('DB_NAME', 'hunterjob.sqlite')
COOKIE_UCA = os.getenv('COOKIE_UCA', '')
APP_ENV = os.getenv('APP_ENV', 'development')
BACKEND_URL = os.getenv('BACKEND_URL', None)

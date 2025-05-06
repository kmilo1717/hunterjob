from dotenv import load_dotenv  # Importar load_dotenv para cargar variables de entorno
import os

load_dotenv()

# Variables de configuración
BROWSER = 'Chrome'  # Puede ser 'Chrome', 'Firefox'
INTEREST_JOBS = ['php', 'laravel', 'frontend', 'backend', 'front end', 'back end', 'desarrollador', 'programador', 'developer', 'software', 'sql']
FILTERS = {
    'MIN_SALARY': 3000000,
    'MODALITY': ['Remoto', 'Presencial y remoto'],
}
EXCLUDE = [
    'bairesdev llc',
    'vendedor',
    'rutas',
    'salesforce',
    'cnc',
    'profesor',
    'almacenista',
    'diseñador',
    'docente',
    'mesa de ayuda',
    'ruta',
    'electrisista',
    'internet',
    'marketing',
    'supervisor',
    'delphi',
    'contador',
    'despachos',
    'electronico',
    'asesor',
    'coordinador',
    'negocios',
    'conductor'
]
HIGHLIGHTS = ['php', 'laravel', 'symfony', '.NET', 'java', 'hibrido', 'presencial', 'spring', 'remoto', 'virtual', 'sql', 'horario', 'contrato', 'contrato:','salario','salario:','años','año', 'angular', 'javascript']

# Variables de configuración
COMPUTRABAJO_URL = 'https://co.computrabajo.com/'

# Variables de entorno cargadas desde el archivo .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_NAME = os.getenv('DB_NAME')
COOKIE_UCA = os.getenv('COOKIE_UCA')
APP_ENV = os.getenv('APP_ENV')
BACKEND_URL = os.getenv('BACKEND_URL')

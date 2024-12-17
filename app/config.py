import os

ALLOWED_FORMATS = ["mp3", "wav"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# Crear el directorio si no existe
os.makedirs(TEMP_DIR, exist_ok=True)
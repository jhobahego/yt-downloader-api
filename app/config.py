import os
from typing import List

ALLOWED_FORMATS = ["mp3", "wav"]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# Lista de proxies gratuitos que podemos rotar
PROXY_LIST: List[str] = [
    # Agrega aquí tus proxies
    # "socks5://user:pass@host:port",
    # "http://host:port",
]

# Crear el directorio si no existe
os.makedirs(TEMP_DIR, exist_ok=True)
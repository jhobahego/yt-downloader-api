import os
from ..config import TEMP_DIR

def cleanup_temp_files():
    """Limpia todos los archivos temporales del directorio temp"""
    for file in os.listdir(TEMP_DIR):
        try:
            os.remove(os.path.join(TEMP_DIR, file))
        except OSError:
            pass

def remove_file(file_path: str):
    """Elimina un archivo específico"""
    try:
        os.remove(file_path)
    except OSError:
        pass
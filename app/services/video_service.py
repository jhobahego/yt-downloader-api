from fastapi import HTTPException
import yt_dlp
import os
import uuid
from ..config import TEMP_DIR, ALLOWED_FORMATS

def download_audio(url: str, format: str) -> str:
    """
    Descarga el audio del video en el formato especificado y retorna la ruta del archivo.
    
    Args:
        url (str): URL del video a descargar.
        format (str): Formato de audio deseado (mp3, wav, etc.).
        
    Returns:
        str: Ruta del archivo de audio descargado.
        
    Raises:
        HTTPException: Si hay un error en la descarga.
    """
    if format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    output_template = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            # ydl.prepare_filename(info) ya incluye TEMP_DIR y extensión
            audio_file = ydl.prepare_filename(info)
            # Cambiar la extensión al formato deseado
            base, _ = os.path.splitext(audio_file)
            audio_file = f"{base}.{format}"
            return audio_file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading audio: {str(e)}")
    

def get_video_info(video_url: str) -> dict:
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_info = {
            'title': info_dict.get('title', 'video'),
            'duration': info_dict.get('duration'),
            'uploader': info_dict.get('uploader'),
            # Puedes agregar más campos si lo deseas
        }
    return video_info


def cleanup_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error removing file {file_path}: {e}")


def validate_url(video_url: str) -> bool:
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Intentar extraer información del video sin descargarlo
            ydl.extract_info(video_url, download=False)
            return True
    except yt_dlp.DownloadError:
        return False
    except Exception:
        return False
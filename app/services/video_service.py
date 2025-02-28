from fastapi import HTTPException
import yt_dlp
import os
import uuid
from ..config import TEMP_DIR, ALLOWED_FORMATS, PROXY_LIST
import random

# Actualizamos las cookies con valores más realistas
YOUTUBE_COOKIES = [
    {
        "name": "CONSENT",
        "value": "YES+yt.452684927.es+FX+917",
        "domain": ".youtube.com",
        "path": "/"
    },
    {
        "name": "VISITOR_INFO1_LIVE",
        "value": "y4-fHXB_Uw4",
        "domain": ".youtube.com",
        "path": "/"
    },
    {
        "name": "YSC",
        "value": "DwKYSlzGJwo",
        "domain": ".youtube.com",
        "path": "/"
    },
    {
        "name": "GPS",
        "value": "1",
        "domain": ".youtube.com",
        "path": "/"
    }
]

def get_cookies_file():
    """Genera un archivo temporal de cookies en formato Netscape"""
    cookies_file = os.path.join(TEMP_DIR, f"cookies_{uuid.uuid4()}.txt")
    
    with open(cookies_file, 'w') as f:
        # Escribir el header necesario para el formato Netscape
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# https://curl.haxx.se/rfc/cookie_spec.html\n")
        f.write("# This is a generated file!  Do not edit.\n\n")
        
        # Escribir cada cookie en el formato correcto
        for cookie in YOUTUBE_COOKIES:
            # Formato: domain flag path secure expiry name value
            f.write(
                f"{cookie['domain']}\t"     # domain
                f"TRUE\t"                    # includesubdomains
                f"{cookie['path']}\t"        # path
                f"FALSE\t"                   # secure
                f"2147483647\t"             # expiry (año 2038)
                f"{cookie['name']}\t"        # name
                f"{cookie['value']}\n"       # value
            )
    
    return cookies_file

def get_random_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

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
    cookies_file = get_cookies_file()
    
    # Configuración base
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'cookiefile': cookies_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192' if format == 'mp3' else '0',
        }],
        'postprocessor_args': [
            '-ar', '44100',
            '-ac', '2',
        ] if format == 'wav' else [],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Range': 'bytes=0-',
            'DNT': '1',
            'Sec-GPC': '1',
        },
        'socket_timeout': 30,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'prefer_insecure': True,
        'cachedir': False,
        'extract_audio': True,
        'audio_format': format,
        'keepvideo': False,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls'],
                'player_client': ['android', 'web'],
            }
        },
        'extractor_retries': 5,
        'file_access_retries': 5,
        'fragment_retries': 5,
        'skip_unavailable_fragments': True,
        'retry_sleep_functions': {
            'http': lambda n: 5,
            'fragment': lambda n: 5,
            'file_access': lambda n: 5,
        },
    }

    proxy = get_random_proxy()
    if proxy:
        ydl_opts['proxy'] = proxy

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url)
                audio_file = ydl.prepare_filename(info)
                base, _ = os.path.splitext(audio_file)
                audio_file = f"{base}.{format}"
                
                # Verificar que el archivo se haya creado correctamente
                if not os.path.exists(audio_file):
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to convert to {format.upper()} format"
                    )
                
                return audio_file
            finally:
                if os.path.exists(cookies_file):
                    os.remove(cookies_file)
    except Exception as e:
        if os.path.exists(cookies_file):
            os.remove(cookies_file)
        print(f"Error downloading audio: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading audio: {str(e)}"
        )

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

def validate_url(video_url: str) -> bool:
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=False)
            return True
    except yt_dlp.utils.DownloadError:
        return False
    except Exception:
        return False

def cleanup_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error removing file {file_path}: {e}")
# YouTube Video Downloader API

API REST desarrollada con FastAPI para descargar audio de videos de YouTube en formatos MP3 y WAV.

## Características

- Descarga de audio en formato MP3 y WAV
- Soporte para extracción de cookies de navegadores (Chrome, Firefox, Opera, Brave)
- Limpieza automática de archivos temporales
- Documentación automática con Swagger UI

## Requisitos Previos

- Python 3.8 o superior
- FFmpeg instalado en el sistema
- pip (gestor de paquetes de Python)
- Un navegador web compatible (Chrome, Firefox, Opera o Brave)

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/yt-downloader-api.git
cd yt-downloader-api
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate # Linux/MacOS
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:

```bash
cp .env.example .env
```

5. Inicia el servidor:

```bash
uvicorn app.main:app --reload
```

6. Accede a la documentación:

```bash
http://localhost:8000/docs
```

## Uso

### Descargar audio de un video

```bash
curl -X POST "http://localhost:8000/download" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Descargar audio de un video con cookies

```bash
curl -X POST "http://localhost:8000/download" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "cookies": "cookie1=value1; cookie2=value2"}'
```

### Descargar audio de un video con cookies de Firefox

```bash
curl -X POST "http://localhost:8000/download" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "cookies": "firefox"}'
```

### Descargar audio de un video con cookies de Chrome

```bash
curl -X POST "http://localhost:8000/download" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "cookies": "chrome"}'
```

### Descargar audio de un video con cookies de Opera

```bash
curl -X POST "http://localhost:8000/download" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "cookies": "opera"}'
```

### Descargar audio de un video con cookies de Brave

```bash
curl -X POST "http://localhost:8000/download" \
-H "Content-Type: application/json" \
-d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "cookies": "brave"}'
```

## Contribución

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/yt-downloader-api.git
cd yt-downloader-api
```

2. Crea una rama:

```bash
git checkout -b tu-rama
```

3. Realiza tus cambios y crea un pull request:

```bash
git add .
git commit -m "Descripción de tus cambios"
git push origin tu-rama
```

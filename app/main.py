from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from .routers import converter
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Video to Audio Converter API",
    description="API para convertir videos a archivos de audio MP3 o WAV",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(converter.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")
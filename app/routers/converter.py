from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from ..services import video_service
from ..config import ALLOWED_FORMATS

router = APIRouter()

@router.get("/download/{video_id}/{format}")
async def download_video(video_id: str, format: str, background_tasks: BackgroundTasks, browser: str):
    if format not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Format must be one of: {', '.join(ALLOWED_FORMATS)}"
        )

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    if not video_service.validate_url(video_url):
        raise HTTPException(status_code=400, detail="Invalid YouTube video URL")

    # Obtener información del video
    video_info = video_service.get_video_info(video_url)
    video_title = video_info['title'].replace('/', '_')

    # Descargar el audio del video en el formato deseado
    audio_file = video_service.download_audio(video_url, format, browser)

    # Programar la limpieza del archivo después de enviar la respuesta
    background_tasks.add_task(video_service.cleanup_file, audio_file)

    # Establecer las cabeceras de respuesta
    headers = {
        "Content-Disposition": f'attachment; filename="{video_title}.{format}"',
        "Content-Type": f"audio/{format}"
    }

    # Devolver el archivo de audio
    return FileResponse(
        path=audio_file,
        media_type=f"audio/{format}",
        filename=f"{video_title}.{format}",
        headers=headers,
    )
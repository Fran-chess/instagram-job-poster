from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
import os
import uuid
from pathlib import Path

from app.core.config import settings

router = APIRouter(prefix="/uploads", tags=["uploads"])

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """Subir una imagen para usar en publicaciones"""
    try:
        # Verificar que el archivo es una imagen
        content_type = file.content_type
        if not content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe ser una imagen"
            )
        
        # Crear un nombre único para el archivo
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Guardar el archivo
        upload_dir = Path(settings.UPLOAD_DIR)
        file_path = upload_dir / unique_filename
        
        # Asegurar que existe el directorio
        os.makedirs(upload_dir, exist_ok=True)
        
        # Escribir el archivo
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Devolver la ruta del archivo guardado
        return {"filename": unique_filename, "path": f"/media/uploads/{unique_filename}"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir la imagen: {str(e)}"
        )

@router.get("/image/{filename}")
async def get_image(filename: str):
    """Obtener una imagen subida previamente"""
    file_path = Path(settings.UPLOAD_DIR) / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )
    
    return FileResponse(file_path)

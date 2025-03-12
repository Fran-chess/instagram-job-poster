# app.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
import uvicorn
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json
import logging
from facebook import GraphAPI  # pip install facebook-sdk

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Instagram Job Poster API")

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar el dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorio para guardar imágenes temporales
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Configuración de Instagram/Facebook
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ID = os.getenv("INSTAGRAM_BUSINESS_ID")

# Modelos de datos
class PostData(BaseModel):
    perfil: str
    ubicacion: str
    email: str
    requisitos: Optional[str] = None

class InstagramResponse(BaseModel):
    success: bool
    message: str
    post_id: Optional[str] = None
    image_url: Optional[str] = None

# Rutas API
@app.post("/api/generate-image", response_model=InstagramResponse)
async def generate_image(
    perfil: str = Form(...),
    ubicacion: str = Form(...),
    email: str = Form(...),
    requisitos: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None)
):
    try:
        # Generar nombre de archivo único
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_path = f"{UPLOAD_DIR}/post_{timestamp}.png"
        
        # Crear imagen base (usando un template o una imagen subida)
        if imagen:
            # Guardar imagen subida
            with open(image_path, "wb") as buffer:
                buffer.write(await imagen.read())
            # Abrir la imagen para modificarla
            img = Image.open(image_path)
        else:
            # Crear imagen desde plantilla
            img = create_template_image()
        
        # Añadir texto a la imagen
        img = add_text_to_image(img, perfil, ubicacion, email, requisitos)
        
        # Guardar imagen final
        img.save(image_path)
        
        return {
            "success": True,
            "message": "Imagen generada correctamente",
            "image_url": f"/uploads/{os.path.basename(image_path)}"
        }
    
    except Exception as e:
        logger.error(f"Error generando imagen: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generando imagen: {str(e)}")

@app.post("/api/publish-to-instagram", response_model=InstagramResponse)
async def publish_to_instagram(
    image_url: str = Form(...),
    caption: Optional[str] = Form(None)
):
    try:
        # Verificar que existe el token de Instagram
        if not INSTAGRAM_ACCESS_TOKEN or not INSTAGRAM_BUSINESS_ID:
            return {
                "success": False,
                "message": "Configuración de Instagram no disponible"
            }
        
        # Ruta completa a la imagen
        image_path = os.path.join(os.getcwd(), image_url.lstrip('/'))
        
        # Publicar en Instagram
        post_id = publish_image_to_instagram(image_path, caption)
        
        return {
            "success": True,
            "message": "Publicado correctamente en Instagram",
            "post_id": post_id
        }
    
    except Exception as e:
        logger.error(f"Error publicando en Instagram: {str(e)}")
        return {
            "success": False,
            "message": f"Error publicando en Instagram: {str(e)}"
        }

# Funciones auxiliares
def create_template_image():
    """Crea una imagen base desde una plantilla predefinida"""
    # Puedes usar una plantilla prediseñada o crear una desde cero
    # Por simplicidad, aquí creamos una imagen en blanco
    width, height = 1080, 1080  # Tamaño recomendado para Instagram
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    
    # Añadir elementos básicos como el logo, fondo, etc.
    # Esto dependerá del diseño específico que necesites
    
    return img

def add_text_to_image(img, perfil, ubicacion, email, requisitos=None):
    """Añade texto a la imagen según el formato deseado"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    try:
        # Intentar cargar fuentes
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 36)
        body_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        # Si no se encuentran las fuentes, usar la predeterminada
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Añadir título "Buscamos Profesionales"
    draw.text((width/2, 100), "Buscamos Profesionales", 
              fill=(0, 51, 102), font=title_font, anchor="mm")
    
    # Añadir perfil
    draw.rectangle([(100, 200), (width-100, 280)], 
                  fill=(0, 204, 153), outline=None)
    draw.text((width/2, 240), perfil.upper(), 
              fill=(0, 0, 0), font=title_font, anchor="mm")
    
    # Añadir ubicación
    draw.text((150, 350), f"📍 {ubicacion}", 
              fill=(0, 0, 0), font=subtitle_font)
    
    # Añadir email
    y_pos = 450
    draw.text((150, y_pos), "Dejanos tu CV:", 
              fill=(0, 0, 0), font=subtitle_font)
    draw.text((150, y_pos + 50), email, 
              fill=(0, 0, 0), font=body_font)
    
    # Añadir requisitos si existen
    if requisitos and requisitos.strip():
        y_pos = 600
        draw.text((150, y_pos), "Requisitos:", 
                  fill=(0, 0, 0), font=subtitle_font)
        
        # Dividir requisitos en líneas si es muy largo
        words = requisitos.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            # Limitar ancho de línea
            if draw.textlength(test_line, font=body_font) > width - 300:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Dibujar líneas de requisitos
        for i, line in enumerate(lines[:3]):  # Limitar a 3 líneas
            draw.text((150, y_pos + 50 + i*40), line, 
                      fill=(0, 0, 0), font=body_font)
    
    # Añadir logo o marca de agua
    # draw.text((width-150, height-50), "DarSalud", 
    #          fill=(0, 153, 153), font=subtitle_font, anchor="rb")
    
    return img

def publish_image_to_instagram(image_path, caption=None):
    """Publica una imagen en Instagram a través de la Graph API"""
    try:
        # Crear mensaje predeterminado si no se proporciona uno
        if not caption:
            caption = "¡Nueva oportunidad laboral! #empleo #trabajo #oportunidad"
        
        # Inicializar el cliente de Graph API
        graph = GraphAPI(access_token=INSTAGRAM_ACCESS_TOKEN)
        
        # 1. Subir la imagen como un contenedor de medios
        with open(image_path, 'rb') as image_file:
            media_object = graph.put_photo(
                image=image_file,
                caption=caption,
                published=False
            )
        
        # 2. Obtener el ID de creación
        creation_id = media_object.get('id')
        
        # 3. Publicar el contenedor como una publicación en Instagram
        result = graph.put_object(
            parent_object=INSTAGRAM_BUSINESS_ID,
            connection_name='media_publish',
            creation_id=creation_id
        )
        
        return result.get('id')
    
    except Exception as e:
        logger.error(f"Error en la publicación en Instagram: {str(e)}")
        raise Exception(f"Error en la publicación: {str(e)}")

# Ruta para servir archivos estáticos (imágenes generadas)
from fastapi.staticfiles import StaticFiles
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Punto de entrada principal
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
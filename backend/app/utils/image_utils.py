# app/utils/image_utils.py
import os
import io
from typing import Tuple, Union, Optional
from PIL import Image, ImageDraw, ImageFont
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

def get_font(font_name: str = "arial.ttf", size: int = 20) -> ImageFont.FreeTypeFont:
    """
    Obtener una fuente para dibujar en imágenes.
    
    Args:
        font_name: Nombre del archivo de fuente
        size: Tamaño de la fuente
        
    Returns:
        Objeto de fuente
    """
    try:
        # Intentar cargar fuente del sistema
        return ImageFont.truetype(font_name, size)
    except OSError:
        # Fallback a fuente por defecto
        logger.warning(f"No se pudo cargar la fuente {font_name}, usando fuente por defecto")
        return ImageFont.load_default()

def calculate_text_position(
    image: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    position: str = "center",
    padding: int = 20
) -> Tuple[int, int]:
    """
    Calcular la posición para un texto en una imagen.
    
    Args:
        image: Imagen donde se dibujará el texto
        text: Texto a dibujar
        font: Fuente a utilizar
        position: Posición del texto ('center', 'top', 'bottom', 'top-left', etc.)
        padding: Padding desde los bordes
        
    Returns:
        Tupla (x, y) con la posición del texto
    """
    width, height = image.size
    text_width = font.getlength(text)
    text_height = font.size
    
    if position == "center":
        return ((width - text_width) // 2, (height - text_height) // 2)
    elif position == "top":
        return ((width - text_width) // 2, padding)
    elif position == "bottom":
        return ((width - text_width) // 2, height - text_height - padding)
    elif position == "top-left":
        return (padding, padding)
    elif position == "top-right":
        return (width - text_width - padding, padding)
    elif position == "bottom-left":
        return (padding, height - text_height - padding)
    elif position == "bottom-right":
        return (width - text_width - padding, height - text_height - padding)
    else:
        return ((width - text_width) // 2, (height - text_height) // 2)

def overlay_text(
    image: Image.Image,
    text: str,
    position: Tuple[int, int],
    font_size: int = 20,
    font_name: str = "arial.ttf",
    color: str = "#000000",
    outline_color: Optional[str] = None,
    outline_width: int = 1
) -> Image.Image:
    """
    Superponer texto en una imagen.
    
    Args:
        image: Imagen donde se dibujará el texto
        text: Texto a dibujar
        position: Posición (x, y) del texto
        font_size: Tamaño de la fuente
        font_name: Nombre del archivo de fuente
        color: Color del texto
        outline_color: Color del contorno (None para sin contorno)
        outline_width: Ancho del contorno
        
    Returns:
        Imagen con el texto superpuesto
    """
    draw = ImageDraw.Draw(image)
    font = get_font(font_name, font_size)
    
    # Si hay contorno, dibujar el texto con offset en todas direcciones
    if outline_color:
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text(
                    (position[0] + offset_x, position[1] + offset_y),
                    text,
                    font=font,
                    fill=outline_color
                )
    
    # Dibujar el texto principal
    draw.text(position, text, font=font, fill=color)
    
    return image

def resize_image(
    image: Union[Image.Image, bytes, str],
    width: Optional[int] = None,
    height: Optional[int] = None,
    keep_aspect_ratio: bool = True
) -> Image.Image:
    """
    Redimensionar una imagen.
    
    Args:
        image: Imagen a redimensionar (objeto PIL, bytes o ruta)
        width: Ancho deseado (None para calcular en base al aspect ratio)
        height: Alto deseado (None para calcular en base al aspect ratio)
        keep_aspect_ratio: Mantener la relación de aspecto
        
    Returns:
        Imagen redimensionada
    """
    # Convertir imagen a objeto PIL si es necesario
    if isinstance(image, bytes):
        img = Image.open(io.BytesIO(image))
    elif isinstance(image, str):
        img = Image.open(image)
    else:
        img = image
    
    if width is None and height is None:
        return img
    
    if keep_aspect_ratio:
        if width is None:
            # Calcular ancho manteniendo la relación de aspecto
            aspect_ratio = img.width / img.height
            width = int(height * aspect_ratio)
        elif height is None:
            # Calcular alto manteniendo la relación de aspecto
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio)
    else:
        # Si no se especifica alguna dimensión, usar la original
        width = width or img.width
        height = height or img.height
    
    return img.resize((width, height), Image.LANCZOS)

def save_image(
    image: Image.Image,
    output_path: str,
    format: str = "PNG",
    quality: int = 95
) -> str:
    """
    Guardar una imagen en disco.
    
    Args:
        image: Imagen a guardar
        output_path: Ruta donde guardar la imagen
        format: Formato de la imagen
        quality: Calidad de la imagen (1-100, solo para JPEG)
        
    Returns:
        Ruta de la imagen guardada
    """
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Guardar imagen
    image.save(output_path, format=format, quality=quality)
    
    return output_path

def get_image_url(image_path: str) -> str:
    """
    Convertir una ruta de archivo a URL para el frontend.
    
    Args:
        image_path: Ruta del archivo de imagen
        
    Returns:
        URL de la imagen
    """
    # Convertir ruta local a URL relativa
    if image_path.startswith(settings.MEDIA_DIR):
        # Quitar el prefijo de la ruta de medios y usar la URL base
        path = image_path[len(settings.MEDIA_DIR):]
        if path.startswith('/'):
            return f"/media{path}"
        else:
            return f"/media/{path}"
    else:
        # Si no está en el directorio de medios, devolver la ruta completa
        return f"/media/{os.path.basename(image_path)}"
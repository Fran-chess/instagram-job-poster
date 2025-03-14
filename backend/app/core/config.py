import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, validator, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "Instagram Job Poster"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """
        Valida y normaliza la configuración de orígenes CORS para soportar múltiples
        formatos de entrada y garantizar la robustez de la aplicación.
        """
        if isinstance(v, str):
            # Si es una cadena JSON, intentar parsearla
            if v.startswith("[") and v.endswith("]"):
                try:
                    import json
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(origin) for origin in parsed]
                except Exception:
                    # En caso de error de parseo, seguir con el siguiente método
                    pass
                
            # Tratar como lista separada por comas
            origins = [origin.strip() for origin in v.strip('"\'').split(",") if origin.strip()]
            return origins
            
        # Si ya es una lista, garantizar que todos los elementos sean strings
        if isinstance(v, list):
            return [str(origin) for origin in v]
            
        # Valor por defecto para casos no manejados
        return []

    # Database
    DB_SERVER: str
    DB_NAME: str
    DB_USERNAME: str 
    DB_PASSWORD: str
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"

    # Instagram API
    INSTAGRAM_USERNAME: str
    INSTAGRAM_PASSWORD: str
    INSTAGRAM_BUSINESS_ACCOUNT_ID: Optional[str] = None
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    
    # Media storage
    MEDIA_DIR: str = "media"
    TEMPLATES_DIR: str = "media/templates"
    GENERATED_DIR: str = "media/generated"
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    # Método para validar los origenes CORS después de la inicialización
    def validate_cors_origins(self):
        """
        Método para validar que los orígenes CORS son URLs válidas y convertirlos
        a objetos AnyHttpUrl si es necesario para middleware CORS.
        """
        validated_origins = []
        for origin in self.BACKEND_CORS_ORIGINS:
            # Asegurar que la URL tenga el protocolo
            if not origin.startswith("http://") and not origin.startswith("https://"):
                origin = f"http://{origin}"
            validated_origins.append(origin)
        return validated_origins

settings = Settings()

# Asegurarse de que los directorios existan
os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)
os.makedirs(settings.GENERATED_DIR, exist_ok=True)
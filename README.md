# Instagram Job Poster

Aplicación para automatizar la creación y publicación de ofertas laborales en Instagram.

## Características

- Creación de publicaciones con datos de ofertas laborales
- Generación automática de imágenes con diseño profesional
- Publicación automatizada en Instagram
- Historial y análisis de publicaciones

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/instagram-job-poster.git
cd instagram-job-poster

# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Instalar dependencias del frontend
cd ../frontend
npm install
```

## Uso

```bash
# Iniciar el backend
cd backend
uvicorn app.main:app --reload

# En otra terminal, iniciar el frontend
cd frontend
npm run dev
```

## Estructura del Proyecto

El proyecto está organizado siguiendo principios de arquitectura limpia y separación de responsabilidades:

- `backend/`: API y servicios (Python/FastAPI)
- `frontend/`: Interfaz de usuario (HTML/JS o React)
- `docs/`: Documentación completa
- `scripts/`: Scripts de utilidad

## Licencia

[MIT](LICENSE)

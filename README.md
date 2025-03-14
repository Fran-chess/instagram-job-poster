# Guía de Implementación de Instagram Job Poster

Esta guía proporciona instrucciones paso a paso para implementar la aplicación Instagram Job Poster.

## Requisitos Previos

- Python 3.8 o superior
- Servidor MSSQL existente
- Driver ODBC para SQL Server
- Cuenta de Instagram (idealmente una cuenta comercial)

## Paso 1: Configuración del Entorno

1. **Clonar el repositorio (o crear las carpetas según la estructura proporcionada)**

```bash
git clone https://github.com/tuusuario/instagram-job-poster.git
cd instagram-job-poster
```

2. **Crear un entorno virtual**

```bash
python -m venv venv
```

3. **Activar el entorno virtual**

En Windows:
```bash
venv\Scripts\activate
```

En macOS/Linux:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**

Copiar el archivo `.env.example` a `.env` y editar con los valores adecuados:

```bash
cp .env.example .env
# Editar .env con tu editor preferido
```

## Paso 2: Configuración de la Base de Datos

1. **Crear tablas e inicializar datos**

```bash
python -m scripts.init_db
```

Este script creará:
- Tablas de la base de datos
- Usuario administrador (usuario: admin, contraseña: admin123)
- Plantillas de ejemplo

## Paso 3: Iniciar la Aplicación en Desarrollo

```bash
python main.py
```

La API estará disponible en `http://localhost:8000`

## Paso 4: Conectar con el Frontend

Asegúrate de que tu frontend esté configurado para conectarse a la API en el punto de acceso correcto (por defecto: `http://localhost:8000/api/v1`).

## Paso 5: Despliegue en Producción

### Opción 1: Servidor Dedicado

1. **Configurar nginx como proxy inverso**

```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /media {
        alias /ruta/a/tu/app/media;
    }
}
```

2. **Configurar el servicio del programador**

Crear un servicio systemd para el programador (en sistemas Linux):

```ini
[Unit]
Description=Instagram Job Poster Scheduler
After=network.target

[Service]
User=tuusuario
WorkingDirectory=/ruta/a/tu/app
ExecStart=/ruta/a/python /ruta/a/tu/app/scripts/scheduler_service.py
Restart=on-failure
Environment=ENVIRONMENT=production

[Install]
WantedBy=multi-user.target
```

3. **Iniciar servicios**

```bash
# Iniciar el servicio web (usando systemd)
sudo systemctl start instagram-job-poster

# Iniciar el servicio del programador
sudo systemctl start instagram-job-poster-scheduler
```

### Opción 2: Despliegue en Docker

1. **Crear el archivo Dockerfile**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar driver ODBC para SQL Server
RUN apt-get update && apt-get install -y curl gnupg2 unixodbc-dev
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

COPY . .

# Crear directorios necesarios
RUN mkdir -p media/templates media/generated

# Exponer puerto
EXPOSE 8000

# Comando para iniciar
CMD ["python", "main.py"]
```

2. **Crear archivo docker-compose.yml**

```yaml
version: '3'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./media:/app/media
    env_file:
      - .env
    environment:
      - ENVIRONMENT=production
    restart: always

  scheduler:
    build: .
    command: python scripts/scheduler_service.py
    volumes:
      - ./media:/app/media
    env_file:
      - .env
    environment:
      - ENVIRONMENT=production
    restart: always
```

3. **Iniciar con Docker Compose**

```bash
docker-compose up -d
```

## Paso 6: Verificación del Despliegue

1. **Verificar que la API está funcionando**

```bash
curl http://localhost:8000/health
# Debería devolver {"status":"ok"}
```

2. **Iniciar sesión en la API**

```bash
curl -X POST http://localhost:8000/api/v1/auth/login -d "username=admin&password=admin123"
# Debería devolver un token de acceso
```

## Notas Importantes

- **Seguridad**: Cambia la contraseña del usuario administrador después del primer inicio de sesión
- **Instagram**: La API de Instagram tiene límites de uso. Evita hacer muchas publicaciones en poco tiempo
- **Imágenes**: Personaliza las plantillas de imagen según el diseño de tu empresa
- **Programación**: Verifica que el programador esté funcionando correctamente

## Solución de Problemas

- **Error de ODBC**: Verifica que el driver ODBC para SQL Server esté instalado y configurado correctamente
- **Error de Instagram**: Si hay problemas con la API de Instagram, verifica las credenciales y el estado de la cuenta
- **Error de base de datos**: Verifica la conexión a la base de datos MSSQL


Flujo de Trabajo Completo
Una vez integrado, el flujo de trabajo será:

El usuario inicia sesión en la aplicación
Selecciona una plantilla y completa el formulario con los datos de la oferta laboral
Genera una vista previa de la publicación
Decide si quiere publicar inmediatamente, programar para más tarde o guardar como borrador
El backend procesa la solicitud y realiza la acción correspondiente

Esta integración permite utilizar todas las funcionalidades del backend que hemos desarrollado, incluyendo:

Gestión de plantillas
Generación de imágenes
Publicación en Instagram
Programación de publicaciones
Historial de publicaciones
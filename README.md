
# API de la Biblioteca

API REST desarrollada con Python y FastAPI para la gestión de libros de una biblioteca.

Proyecto Integrador del Módulo 3 - Bootcamp Python Backend de Silicon Misiones.

## Tecnologías utilizadas

- Python 3.14
- FastAPI
- Pydantic
- Uvicorn
- JSON
- Logging
- Ruff
- Git y GitHub

## Funcionalidades

- CRUD de libros.
- Validación de datos con Pydantic.
- Filtros, búsqueda y paginación.
- Control de libros duplicados.
- Préstamos y devoluciones.
- Estadísticas de la biblioteca.
- Persistencia de datos en JSON.
- Registro de eventos con logging.
- Documentación automática con Swagger.

## Estructura del proyecto

```text
api-biblioteca/
├── main.py
├── schemas.py
├── datos.py
├── datos/
│   └── libros.json
├── requirements.txt
├── README.md
└── .gitignore
```

- `main.py`: configuración y endpoints de la API.
- `schemas.py`: modelos y validaciones de datos.
- `datos.py`: administración y persistencia de datos.
- `datos/libros.json`: almacenamiento de libros.
- `requirements.txt`: dependencias del proyecto.
- `.gitignore`: archivos y carpetas excluidos de Git.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/sergasgoi/api-biblioteca.git
cd api-biblioteca
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

Si el comando `python` no es reconocido en Windows, utilizar:

```powershell
py -m venv venv
```

### 3. Activar el entorno virtual

En Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar el servidor:

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Para detener el servidor, presionar `Ctrl+C`.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Mensaje de bienvenida |
| GET | `/libros` | Listar libros |
| GET | `/libros/buscar` | Buscar libros por título o autor |
| GET | `/libros/estadisticas` | Consultar estadísticas |
| GET | `/libros/{id}` | Consultar libro por ID |
| POST | `/libros` | Crear libro |
| PUT | `/libros/{id}` | Actualizar libro completamente |
| PATCH | `/libros/{id}` | Actualizar libro parcialmente |
| DELETE | `/libros/{id}` | Eliminar libro |
| POST | `/libros/{id}/prestar` | Prestar libro |
| POST | `/libros/{id}/devolver` | Devolver libro |

## Persistencia de datos

Los datos se guardan automáticamente en `datos/libros.json`
después de cada modificación y se recuperan al iniciar la API.

Si el archivo no existe, está vacío o contiene JSON inválido,
la aplicación inicia con una biblioteca vacía.

## Logging

Los eventos y advertencias de la aplicación se registran
en el archivo `api.log`.

## Archivos excluidos

El archivo `.gitignore` excluye los siguientes archivos y
directorios del repositorio:

- `venv/`
- `.venv/`
- `__pycache__/`
- `*.pyc`
- `.ruff_cache/`
- `api.log`

## Calidad de código

Instalar Ruff:

```bash
pip install ruff
```

Verificar el código:

```bash
ruff check .
```

Resultado esperado:

```text
All checks passed!
```

Verificar la importación de la aplicación:

```bash
python -c "import main"
```

Este comando debe finalizar sin errores y sin mostrar
mensajes en la consola.

## Autor

**Sergio Gastón Goi**

Bootcamp Python Backend - Silicon Misiones.

Proyecto Integrador - Módulo 3 - 2026.

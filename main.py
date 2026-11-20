from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

libros = []
siguiente_id = 1

class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    autor: str = Field(min_length=3, max_length=60)
    anio: int = Field(ge=1000, le=2100)
    disponible: bool = True

@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}

@app.get("/libros")
def listar_libros():
    return libros

@app.post("/libros", status_code=201)
def crear_libro(libro: LibroEntrada):
    global siguiente_id
    nuevo_libro = {
        "id": siguiente_id,
        **libro.model_dump()
    }
    libros.append(nuevo_libro)
    siguiente_id += 1
    return nuevo_libro



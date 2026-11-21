from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import json

RUTA_ARCHIVO = Path(__file__).parent / "datos" / "libros.json"

app = FastAPI()

libros = []
siguiente_id = 1


def guardar_libros():
    RUTA_ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(libros, archivo, ensure_ascii=False, indent=4)


def cargar_libros():
    global libros, siguiente_id

    try:
        with open(RUTA_ARCHIVO, "r", encoding="utf-8") as archivo:
            libros = json.load(archivo)

        if not isinstance(libros, list):
            libros = []

        siguiente_id = max(
            (libro["id"] for libro in libros),
            default=0
        ) + 1

    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError, KeyError):
        libros = []
        siguiente_id = 1


cargar_libros()


class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    autor: str = Field(min_length=3, max_length=60)
    anio: int = Field(ge=1000, le=2100)
    disponible: bool = True


class LibroActualizar(BaseModel):
    titulo: str | None = Field(default=None,min_length=3,max_length=100)
    autor: str | None = Field(default=None,min_length=3,max_length=60)
    anio: int | None = Field( default=None,ge=1000,le=2100)
    disponible: bool | None = None


@app.get("/")
def inicio():
    return {"mensaje": "API de la biblioteca"}


@app.get("/libros")
def listar_libros(
    autor: str | None = None,
    disponible: bool | None = None,
    desde: int = 0,
    limite: int = 100    
):
    resultado = sorted(libros, key=lambda libro: libro["id"])

    if autor is not None:
        resultado = [
            libro for libro in resultado
            if libro["autor"].lower() == autor.lower()
        ]

    if disponible is not None:
        resultado = [
            libro for libro in resultado
            if libro["disponible"] == disponible
        ]

    return resultado[desde:desde + limite]


@app.post("/libros", status_code=201)
def crear_libro(libro: LibroEntrada):
    global siguiente_id

    for libro_existente in libros:
        if (
            libro_existente["titulo"].lower() == libro.titulo.lower()
            and libro_existente["autor"].lower() == libro.autor.lower()
        ):
            raise HTTPException(
                status_code=409,
                detail="Ya existe un libro con ese titulo y autor"
            )

    nuevo_libro = {
        "id": siguiente_id,
        **libro.model_dump()
    }

    libros.append(nuevo_libro)
    siguiente_id += 1
    guardar_libros()

    return nuevo_libro


@app.get("/libros/{id}")
def obtener_libro(id: int):

    for libro in libros:
        if libro["id"] == id:
            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.delete("/libros/{id}", status_code=204)
def eliminar_libro(id: int):
    for libro in libros:
        if libro["id"] == id:
            libros.remove(libro)

            guardar_libros()

            return

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.put("/libros/{id}")
def actualizar_libro(id: int, libro_actualizado: LibroEntrada):

    for indice, libro in enumerate(libros):
        if libro["id"] == id:

            libros[indice] = {
                "id": id,
                **libro_actualizado.model_dump()
            }

            guardar_libros()

            return libros[indice]

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.patch("/libros/{id}")
def actualizar_libro_parcial(id: int, cambios: LibroActualizar):

    for libro in libros:
        if libro["id"] == id:

            datos_actualizados = cambios.model_dump(exclude_unset=True)

            for campo, valor in datos_actualizados.items():
                if valor is None:
                    raise HTTPException(
                        status_code=422,
                        detail=f"El campo {campo} no puede ser null"
                    )

            libro.update(datos_actualizados)

            guardar_libros()

            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

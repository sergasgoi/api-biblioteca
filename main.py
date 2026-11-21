from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

libros = []
siguiente_id = 1


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
    resultado = libros.copy()

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
    nuevo_libro = {
        "id": siguiente_id,
        **libro.model_dump()
    }
    libros.append(nuevo_libro)
    siguiente_id += 1
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
            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

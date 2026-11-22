import logging

from fastapi import FastAPI, HTTPException, Query

import datos
from schemas import LibroActualizar, LibroEntrada

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    filename="api.log",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("API de biblioteca iniciada")

@app.get("/", summary="Mostrar Mensaje de Bienvenida")
def inicio():
    return {"mensaje": "API de la biblioteca"}


@app.post("/libros", status_code=201, summary="Registrar un Nuevo Libro")
def crear_libro(libro: LibroEntrada):
    global siguiente_id

    for libro_existente in datos.libros:
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

    datos.libros.append(nuevo_libro)
    siguiente_id += 1
    datos.guardar_libros()

    logger.info(f"Libro {nuevo_libro['id']} creado")

    return nuevo_libro


@app.get("/libros", summary="Listar Libros con Filtros y Paginación")
def listar_libros(
    autor: str | None = None,
    disponible: bool | None = None,
    desde: int = Query(default=0, ge=0),
    limite: int = Query(default=100, ge=1)   
):
    resultado = sorted(datos.libros, key=lambda libro: libro["id"])

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


@app.get("/libros/buscar", summary="Buscar Libros por Título o Autor")
def buscar_libros(texto: str):

    resultado = []

    for libro in datos.libros:
        if (
            texto.lower() in libro["titulo"].lower()
            or texto.lower() in libro["autor"].lower()
        ):
            resultado.append(libro)

    return resultado


@app.get("/libros/estadisticas", summary="Consultar Estadísticas de la Biblioteca")
def obtener_estadisticas():

    total = len(datos.libros)
    disponibles = 0
    prestados = 0

    for libro in datos.libros:
        if libro["disponible"]:
            disponibles += 1
        else:
            prestados += 1

    return {
        "total": total,
        "disponibles": disponibles,
        "prestados": prestados
    }


@app.get("/libros/{id}", summary="Consultar un Libro por su ID")
def obtener_libro(id: int):

    for libro in datos.libros:
        if libro["id"] == id:
            return libro

    logger.warning(f"Libro {id} no encontrado")

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.delete("/libros/{id}", status_code=204, summary="Eliminar un Libro")
def eliminar_libro(id: int):
    for libro in datos.libros:
        if libro["id"] == id:
            datos.libros.remove(libro)

            datos.guardar_libros()

            return

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.put("/libros/{id}", summary="Actualizar Completamente un Libro")
def actualizar_libro(id: int, libro_actualizado: LibroEntrada):

    for indice, libro in enumerate(datos.libros):
        if libro["id"] == id:

            datos.libros[indice] = {
                "id": id,
                **libro_actualizado.model_dump()
            }

            datos.guardar_libros()

            return datos.libros[indice]

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.patch("/libros/{id}", summary="Actualizar Parcialmente un Libro")
def actualizar_libro_parcial(id: int, cambios: LibroActualizar):

    for libro in datos.libros:
        if libro["id"] == id:

            datos_actualizados = cambios.model_dump(exclude_unset=True)

            for campo, valor in datos_actualizados.items():
                if valor is None:
                    raise HTTPException(
                        status_code=422,
                        detail=f"El campo {campo} no puede ser null"
                    )

            libro.update(datos_actualizados)

            datos.guardar_libros()

            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.post("/libros/{id}/prestar", summary="Prestar un Libro Disponible")
def prestar_libro(id: int):

    for libro in datos.libros:
        if libro["id"] == id:

            if not libro["disponible"]:
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está prestado"
                )

            libro["disponible"] = False
            datos.guardar_libros()

            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.post("/libros/{id}/devolver", summary="Devolver un Libro Prestado")
def devolver_libro(id: int):

    for libro in datos.libros:
        if libro["id"] == id:

            if libro["disponible"]:
                raise HTTPException(
                    status_code=409,
                    detail="El libro ya está disponible"
                )

            libro["disponible"] = True
            datos.guardar_libros()

            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

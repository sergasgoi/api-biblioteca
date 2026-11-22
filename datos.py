import json
from pathlib import Path

RUTA_ARCHIVO = Path(__file__).parent / "datos" / "libros.json"

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

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        ValueError,
        TypeError,
        KeyError
    ):
        libros = []
        siguiente_id = 1


cargar_libros()

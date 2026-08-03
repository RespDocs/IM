import json
import os

ARCHIVO_INVENTARIO = (
    "inventario_detalle.json"
)

with open(
    "impresoras.json",
    "r",
    encoding="utf-8"
) as f:

    impresoras = json.load(f)

if os.path.exists(
    ARCHIVO_INVENTARIO
):

    with open(
        ARCHIVO_INVENTARIO,
        "r",
        encoding="utf-8"
    ) as f:

        inventario = json.load(f)

else:

    inventario = {}

for impresora in impresoras[
    "impresoras"
]:

    serial = impresora[
        "serial"
    ]

    if serial not in inventario:

        inventario[
            serial
        ] = {

            "referencia": "",

            "departamento": "",

            "contacto": "",

            "instalacion": ""

        }

with open(
    ARCHIVO_INVENTARIO,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        inventario,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"{ARCHIVO_INVENTARIO} actualizado"
)
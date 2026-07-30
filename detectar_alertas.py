import json
import os
from datetime import datetime


# --------------------------------------------------
# CARGA ARCHIVOS
# --------------------------------------------------

with open(
    "estado.json",
    "r",
    encoding="utf-8"
) as f:

    estado = json.load(f)

with open(
    "alertas.json",
    "r",
    encoding="utf-8"
) as f:

    alertas = json.load(f)

with open(
    "alertas_config.json",
    "r",
    encoding="utf-8"
) as f:

    config = json.load(f)


# --------------------------------------------------
# CONFIG ALERTAS
# --------------------------------------------------

advertencia = config["default"]["advertencia"]
critico = config["default"]["critico"]


# --------------------------------------------------
# CONTROL IDS
# --------------------------------------------------

if os.path.exists(
    "control_alertas.json"
):

    with open(
        "control_alertas.json",
        "r",
        encoding="utf-8"
    ) as f:

        control = json.load(f)

else:

    control = {
        "ultimo_id": 0
    }


def generar_id_alerta():

    control["ultimo_id"] += 1

    return (
        f"UAH_"
        f"{control['ultimo_id']:05d}"
    )


# --------------------------------------------------
# RECORRER IMPRESORAS
# --------------------------------------------------

for impresora in estado["impresoras"]:

    nombre = impresora["nombre"]
    modelo = impresora["modelo"]
    serial = impresora["serial"]

    # --------------------------------------------------
    # OFFLINE
    # --------------------------------------------------

    if not impresora.get(
        "online",
        True
    ):

        existe = any(

            a.get("equipo") == nombre
            and a.get("tipo") == "offline"
            and a.get("estado") == "notificado"

            for a in alertas["alertas"]

        )

        if not existe:

            nueva_alerta = {

                "id_alerta":
                    generar_id_alerta(),

                "equipo":
                    nombre,

                "serial":
                    serial,

                "modelo":
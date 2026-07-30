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
                    modelo,

                "tipo":
                    "offline",

                "estado":
                    "notificado",

                "fecha_notificacion":
                    datetime.now().isoformat()

            }

            alertas["alertas"].append(
                nueva_alerta
            )

            print(
                f"OFFLINE - "
                f"{nueva_alerta['id_alerta']} - "
                f"{nombre}"
            )

        continue

    # --------------------------------------------------
    # CONSUMIBLES
    # --------------------------------------------------

    consumibles = impresora.get(
        "consumibles",
        {}
    )

    for consumible, porcentaje in consumibles.items():

        criticidad = None

        if porcentaje <= critico:

            criticidad = "critico"

        elif porcentaje <= advertencia:

            criticidad = "advertencia"

        else:

            continue

        existe = any(

            a.get("equipo") == nombre

            and

            a.get("consumible") == consumible

            and

            a.get("estado") == "notificado"

            for a in alertas["alertas"]

        )

        if existe:

            continue

        nueva_alerta = {

            "id_alerta":
                generar_id_alerta(),

            "equipo":
                nombre,

            "serial":
                serial,

            "modelo":
                modelo,

            "tipo":
                "consumible",

            "consumible":
                consumible,

            "porcentaje":
                porcentaje,

            "criticidad":
                criticidad,

            "estado":
                "notificado",

            "fecha_notificacion":
                datetime.now().isoformat()

        }

        alertas["alertas"].append(
            nueva_alerta
        )

        print(

            f"{criticidad.upper()} - "

            f"{nueva_alerta['id_alerta']} - "

            f"{nombre} - "

            f"{consumible} "

            f"({porcentaje}%)"

        )


# --------------------------------------------------
# GUARDAR ALERTAS
# --------------------------------------------------

with open(
    "alertas.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        alertas,
        f,
        indent=2,
        ensure_ascii=False
    )


# --------------------------------------------------
# GUARDAR CONTROL IDS
# --------------------------------------------------

with open(
    "control_alertas.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        control,
        f,
        indent=2,
        ensure_ascii=False
    )


print()
print(
    "alertas.json actualizado"
)
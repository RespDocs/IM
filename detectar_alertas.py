import json
import os
from datetime import datetime

# --------------------------------------------------
# CARGA ARCHIVOS
# --------------------------------------------------

def cargar_json(nombre, defecto):

    if os.path.exists(nombre):

        with open(
            nombre,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return defecto


estado = cargar_json(
    "estado.json",
    {"impresoras": []}
)

alertas = cargar_json(
    "alertas.json",
    {"alertas": []}
)

config = cargar_json(
    "alertas_config.json",
    {
        "default": {
            "advertencia": 20,
            "critico": 10
        }
    }
)

control = cargar_json(
    "control_alertas.json",
    {
        "ultimo_id": 0
    }
)

gestion = cargar_json(
    "gestion_alertas.json",
    {}
)

# --------------------------------------------------
# CONFIG ALERTAS
# --------------------------------------------------

advertencia = config["default"]["advertencia"]
critico = config["default"]["critico"]

# --------------------------------------------------
# GENERADOR IDS
# --------------------------------------------------

def generar_id_alerta():

    control["ultimo_id"] += 1

    return (
        f"UAH_"
        f"{control['ultimo_id']:05d}"
    )


# --------------------------------------------------
# INDEXAR ALERTAS EXISTENTES
# --------------------------------------------------

alertas_consumibles = {}

for alerta in alertas["alertas"]:

    if alerta.get("tipo") != "consumible":
        continue

    clave = alerta.get(
        "clave_alerta"
    )

    if clave:

        alertas_consumibles[
            clave
        ] = alerta

# --------------------------------------------------
# RECORRER IMPRESORAS
# --------------------------------------------------

for impresora in estado.get(
    "impresoras",
    []
):

    nombre = impresora.get(
        "nombre"
    )

    modelo = impresora.get(
        "modelo"
    )

    serial = impresora.get(
        "serial"
    )

    online = impresora.get(
        "online",
        True
    )

    # --------------------------------------------------
    # OFFLINE
    # --------------------------------------------------

    if not online:

        existe = any(

            a.get("tipo") == "offline"

            and

            a.get("serial") == serial

            and

            a.get("estado") == "notificado"

            for a in alertas["alertas"]

        )

        if not existe:

            alertas["alertas"].append({

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

            })

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

        clave_alerta = (
            f"{serial}_"
            f"{consumible}"
        )

        # ------------------------------------------
        # ALERTA EXISTENTE
        # ------------------------------------------

        if clave_alerta in alertas_consumibles:

            alerta = alertas_consumibles[
                clave_alerta
            ]

            alerta[
                "porcentaje"
            ] = porcentaje

            alerta[
                "criticidad"
            ] = criticidad

            alerta[
                "modelo"
            ] = modelo

            alerta[
                "equipo"
            ] = nombre

            continue

        # ------------------------------------------
        # NUEVA ALERTA
        # ------------------------------------------

        nuevo_id = generar_id_alerta()

        nueva_alerta = {

            "id_alerta":
                nuevo_id,

            "clave_alerta":
                clave_alerta,

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

        alertas_consumibles[
            clave_alerta
        ] = nueva_alerta

        # ------------------------------------------
        # GESTION
        # ------------------------------------------

        gestion[
            nuevo_id
        ] = {

            "estado": 1,

            "fecha_actualizacion":
                datetime.now().isoformat(),

            "observacion": ""

        }

        print(

            f"{criticidad.upper()} - "

            f"{nuevo_id} - "

            f"{nombre} - "

            f"{consumible} "

            f"({porcentaje}%)"

        )

# --------------------------------------------------
# GUARDAR ALERTAS
# --------------------------------------------------

print()
print("TOTAL ALERTAS:")
print(len(alertas["alertas"]))
print()

for a in alertas["alertas"][:3]:
    print(a)

print()

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

# --------------------------------------------------
# GUARDAR GESTION
# --------------------------------------------------

with open(
    "gestion_alertas.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        gestion,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print(
    "alertas.json actualizado"
)
import json
from datetime import datetime

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

advertencia = config["default"]["advertencia"]
critico = config["default"]["critico"]

for impresora in estado["impresoras"]:

    nombre = impresora["nombre"]
    modelo = impresora["modelo"]

    # OFFLINE

    if not impresora.get("online", True):

        existe = any(

            a.get("equipo") == nombre
            and a.get("tipo") == "offline"
            and a.get("estado") == "notificado"

            for a in alertas["alertas"]

        )

        if not existe:

            alertas["alertas"].append({

                "equipo": nombre,

                "modelo": modelo,

                "tipo": "offline",

                "estado": "notificado",

                "fecha_notificacion":
                    datetime.now().isoformat()

            })

            print(
                f"Offline: {nombre}"
            )

        continue

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
            and a.get("consumible") == consumible
            and a.get("estado") == "notificado"

            for a in alertas["alertas"]

        )

        if existe:
            continue

        alertas["alertas"].append({

            "equipo":
                nombre,

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

        })

        print(
            f"{criticidad.upper()} - "
            f"{nombre} - "
            f"{consumible} "
            f"({porcentaje}%)"
        )

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

print()
print(
    "alertas.json actualizado"
)
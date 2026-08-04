import json
from datetime import datetime

ARCHIVO_EVENTOS = "eventos.json"


def cargar(nombre):

    try:

        with open(
            nombre,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}


# -------------------------------------------------
# CARGA
# -------------------------------------------------

estado_anterior = cargar(
    "estado_anterior.json"
)

estado_actual = cargar(
    "estado.json"
)

eventos = cargar(
    ARCHIVO_EVENTOS
)

if not isinstance(
    eventos,
    list
):

    eventos = []


# -------------------------------------------------
# INDICES POR SERIAL
# -------------------------------------------------

anteriores = {

    str(
        i.get("serial")
    ).strip(): i

    for i in estado_anterior.get(
        "impresoras",
        []
    )

    if i.get("serial")

}

actuales = {

    str(
        i.get("serial")
    ).strip(): i

    for i in estado_actual.get(
        "impresoras",
        []
    )

    if i.get("serial")

}


# -------------------------------------------------
# COMPARACION
# -------------------------------------------------

eventos_nuevos = 0

for serial, actual in actuales.items():

    anterior = anteriores.get(
        serial
    )

    if not anterior:
        continue

    fecha = datetime.now().isoformat()

    nombre = actual.get(
        "nombre",
        serial
    )

    # -------------------------------------
    # CAMBIO DE IP
    # -------------------------------------

    ip_anterior = anterior.get(
        "ip"
    )

    ip_actual = actual.get(
        "ip"
    )

    if (

        ip_anterior

        and

        ip_actual

        and

        ip_anterior != ip_actual

    ):

        eventos.append({

            "fecha":
                fecha,

            "tipo":
                "cambio_ip",

            "equipo":
                nombre,

            "serial":
                serial,

            "detalle":
                f"{ip_anterior} → {ip_actual}"

        })

        eventos_nuevos += 1

        print(
            f"Cambio IP: "
            f"{nombre}"
        )

    # -------------------------------------
    # OFFLINE
    # -------------------------------------

    if (

        anterior.get(
            "online"
        ) is True

        and

        actual.get(
            "online"
        ) is False

    ):

        eventos.append({

            "fecha":
                fecha,

            "tipo":
                "offline",

            "equipo":
                nombre,

            "serial":
                serial,

            "detalle":
                "Equipo sin respuesta"

        })

        eventos_nuevos += 1

        print(
            f"Offline: "
            f"{nombre}"
        )

    # -------------------------------------
    # ONLINE
    # -------------------------------------

    if (

        anterior.get(
            "online"
        ) is False

        and

        actual.get(
            "online"
        ) is True

    ):

        eventos.append({

            "fecha":
                fecha,

            "tipo":
                "online",

            "equipo":
                nombre,

            "serial":
                serial,

            "detalle":
                "Equipo recuperado"

        })

        eventos_nuevos += 1

        print(
            f"Online: "
            f"{nombre}"
        )


# -------------------------------------------------
# GUARDAR
# -------------------------------------------------

with open(

    ARCHIVO_EVENTOS,

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        eventos,

        f,

        indent=2,

        ensure_ascii=False

    )

print()

print(
    f"Eventos nuevos: "
    f"{eventos_nuevos}"
)

print(
    f"Eventos acumulados: "
    f"{len(eventos)}"
)

print(
    "eventos.json actualizado"
)
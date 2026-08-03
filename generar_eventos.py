import json
from datetime import datetime


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


# -------------------------
# CARGA
# -------------------------

estado_anterior = cargar(
    "estado_anterior.json"
)

estado_actual = cargar(
    "estado.json"
)

eventos = cargar(
    "eventos.json"
)

if not isinstance(
    eventos,
    list
):

    eventos = []


# -------------------------
# INDICES POR SERIAL
# -------------------------

anteriores = {

    i.get("serial"): i

    for i in estado_anterior.get(
        "impresoras",
        []
    )

}

actuales = {

    i.get("serial"): i

    for i in estado_actual.get(
        "impresoras",
        []
    )

}


# -------------------------
# COMPARACION
# -------------------------

for serial, actual in actuales.items():

    anterior = anteriores.get(
        serial
    )

    if not anterior:
        continue

    fecha = datetime.now().isoformat()

    nombre = actual.get(
        "nombre"
    )

    # -------------------------
    # CAMBIO DE IP
    # -------------------------

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

            "fecha": fecha,

            "tipo": "cambio_ip",

            "equipo": nombre,

            "serial": serial,

            "ip_anterior":
                ip_anterior,

            "ip_nueva":
                ip_actual

        })

        print(
            f"Cambio IP: {nombre}"
        )

    # -------------------------
    # OFFLINE
    # -------------------------

    if (
        anterior.get("online")
        is True
        and
        actual.get("online")
        is False
    ):

        eventos.append({

            "fecha": fecha,

            "tipo": "offline",

            "equipo": nombre,

            "serial": serial,

            "ip": ip_actual

        })

        print(
            f"Offline: {nombre}"
        )

    # -------------------------
    # ONLINE
    # -------------------------

    if (
        anterior.get("online")
        is False
        and
        actual.get("online")
        is True
    ):

        eventos.append({

            "fecha": fecha,

            "tipo": "online",

            "equipo": nombre,

            "serial": serial,

            "ip": ip_actual

        })

        print(
            f"Recuperado: {nombre}"
        )


# -------------------------
# GUARDAR
# -------------------------

with open(
    "eventos.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        eventos,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Eventos registrados: {len(eventos)}"
)
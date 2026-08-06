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

instalaciones_anterior = cargar(
    "instalaciones_anterior.json"
)

instalaciones_actual = cargar(
    "instalaciones.json"
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
# INSTALACIONES
# -------------------------------------------------

anteriores_inst = {

    (
        i.get("equipo"),
        i.get("consumible"),
        i.get("contador_instalacion")
    )

    for i in instalaciones_anterior.get(
        "instalaciones",
        []
    )

}

for instalacion in instalaciones_actual.get(
    "instalaciones",
    []
):

    clave = (

        instalacion.get("equipo"),

        instalacion.get("consumible"),

        instalacion.get(
            "contador_instalacion"
        )

    )

    if clave in anteriores_inst:
        continue

    eventos.append({

        "fecha":
            instalacion.get(
                "fecha_instalacion",
                datetime.now().isoformat()
            ),

        "tipo":
            "instalacion",

        "equipo":
            instalacion.get("serial")
            or instalacion.get("equipo")
            or instalacion.get("ip")
            or "Sin identificar",

        "detalle":
            (
                f"{instalacion.get('consumible')} "
                f"reemplazado"
            )

    })

    eventos_nuevos += 1

    print(

        "Instalacion: "

        +

        str(
            instalacion.get(
                "equipo"
            )
        )

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
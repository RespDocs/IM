import json
from datetime import datetime

LIMITE_ANTERIOR = 70
LIMITE_NUEVO = 90


def cargar_json(nombre, defecto):

    try:

        with open(
            nombre,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return defecto


estado_anterior = cargar_json(
    "estado_anterior.json",
    None
)

if estado_anterior is None:

    print(
        "No existe estado_anterior.json"
    )

    exit()


estado_actual = cargar_json(
    "estado.json",
    {"impresoras": []}
)

catalogo = cargar_json(
    "catalogo_consumibles.json",
    {}
)

instalaciones = cargar_json(
    "instalaciones.json",
    {"instalaciones": []}
)

eventos = cargar_json(
    "eventos.json",
    []
)


equipos_anteriores = {}

for equipo in estado_anterior["impresoras"]:

    equipos_anteriores[
        equipo["nombre"]
    ] = equipo


for equipo_actual in estado_actual["impresoras"]:

    nombre = equipo_actual["nombre"]

    if nombre not in equipos_anteriores:
        continue

    equipo_anterior = equipos_anteriores[
        nombre
    ]

    consumibles_actuales = equipo_actual.get(
        "consumibles",
        {}
    )

    consumibles_anteriores = equipo_anterior.get(
        "consumibles",
        {}
    )

    for consumible, valor_actual in consumibles_actuales.items():

        valor_anterior = consumibles_anteriores.get(
            consumible
        )

        if valor_anterior is None:
            continue

        if (

            valor_anterior < LIMITE_ANTERIOR

            and

            valor_actual > LIMITE_NUEVO

        ):

            modelo = equipo_actual["modelo"]

            pn = None
            vida_nominal = None

            if modelo in catalogo:

                if consumible in catalogopn = (
                        catalogo[modelo]
                        [consumible]
                        .get("pn")
                    )

                    vida_nominal = (
                        catalogo[modelo]
                        [consumible]
                        .get("vida_nominal")
                    )

            duplicado = False

            for item in instalaciones[
                "instalaciones"
            ]:

                if (

                    item["equipo"] == nombre

                    and

                    item["consumible"]
                    == consumible

                    and

                    item[
                        "contador_instalacion"
                    ]
                    == equipo_actual["contador"]

                ):

                    duplicado = True
                    break

            if duplicado:
                continue

            evento = {

                "equipo":
                    nombre,

                "modelo":
                    modelo,

                "consumible":
                    consumible,

                "pn":
                    pn,

                "vida_nominal":
                    vida_nominal,

                "fecha_instalacion":
                    datetime.now().isoformat(),

                "contador_instalacion":
                    equipo_actual["contador"],

                "porcentaje_instalacion":
                    valor_actual,

                "origen":
                    "auto_detectado"

            }

            instalaciones[
                "instalaciones"
            ].append(
                evento
            )

            eventos.append({

                "fecha":
                    datetime.now().isoformat(),

                "tipo":
                    "instalacion",

                "equipo":
                    nombre,

                "modelo":
                    modelo,

                "consumible":
                    consumible,

                "detalle":
                    f"{consumible} reemplazado"

            })

            print(
                f"Cambio detectado: "
                f"{nombre} - {consumible}"
            )


with open(
    "instalaciones.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        instalaciones,
        f,
        indent=2,
        ensure_ascii=False
    )


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


print()
print(
    "instalaciones.json actualizado"
)
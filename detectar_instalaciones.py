import json
from datetime import datetime

LIMITE_ANTERIOR = 70
LIMITE_NUEVO = 90

try:

    with open(
        "estado_anterior.json",
        "r",
        encoding="utf-8"
    ) as f:

        estado_anterior = json.load(f)

except:

    print(
        "No existe estado_anterior.json"
    )

    exit()

with open(
    "estado.json",
    "r",
    encoding="utf-8"
) as f:

    estado_actual = json.load(f)

with open(
    "catalogo_consumibles.json",
    "r",
    encoding="utf-8"
) as f:

    catalogo = json.load(f)

with open(
    "instalaciones.json",
    "r",
    encoding="utf-8"
) as f:

    instalaciones = json.load(f)

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

                if consumible in catalogo[modelo]:

                    pn = (
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
                    item["consumible"] == consumible
                    and
                    item["contador_instalacion"]
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

print()
print(
    "instalaciones.json actualizado"
)
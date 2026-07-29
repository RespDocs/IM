import json

with open(
    "estado.json",
    "r",
    encoding="utf-8"
) as f:

    estado = json.load(f)

with open(
    "instalaciones.json",
    "r",
    encoding="utf-8"
) as f:

    instalaciones = json.load(f)

resultado = []

equipos = {}

for impresora in estado["impresoras"]:

    equipos[
        impresora["nombre"]
    ] = impresora

for instalacion in instalaciones["instalaciones"]:

    equipo = instalacion["equipo"]

    if equipo not in equipos:
        continue

    estado_equipo = equipos[equipo]

    contador_actual = estado_equipo["contador"]

    contador_instalacion = \
        instalacion["contador_instalacion"]

    vida_nominal = \
        instalacion.get("vida_nominal")

    if vida_nominal is None:
        continue

    uso_real = (
        contador_actual
        - contador_instalacion
    )

    restante = (
        vida_nominal
        - uso_real
    )

    if restante < 0:
        restante = 0

    restante_pct = round(
        restante * 100 / vida_nominal
    )

    resultado.append({

        "equipo":
            equipo,

        "modelo":
            instalacion["modelo"],

        "consumible":
            instalacion["consumible"],

        "pn":
            instalacion["pn"],

        "vida_nominal":
            vida_nominal,

        "contador_instalacion":
            contador_instalacion,

        "contador_actual":
            contador_actual,

        "uso_real":
            uso_real,

        "restante":
            restante,

        "restante_pct":
            restante_pct

    })

salida = {

    "consumibles":
        resultado

}

with open(
    "vida_consumibles.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        salida,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    "vida_consumibles.json generado"
)
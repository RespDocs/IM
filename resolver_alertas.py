import json
from datetime import datetime

with open(
    "alertas.json",
    "r",
    encoding="utf-8"
) as f:

    alertas = json.load(f)

with open(
    "instalaciones.json",
    "r",
    encoding="utf-8"
) as f:

    instalaciones = json.load(f)

cambios = 0

for alerta in alertas["alertas"]:

    if alerta["estado"] != "notificado":
        continue

    for instalacion in instalaciones["instalaciones"]:

        if (
            alerta["equipo"]
            == instalacion["equipo"]
            and
            alerta["consumible"]
            == instalacion["consumible"]
        ):

            alerta["estado"] = "instalado"

            alerta["fecha_instalacion"] = \
                instalacion["fecha_instalacion"]

            alerta["contador_instalacion"] = \
                instalacion["contador_instalacion"]

            alerta["porcentaje_reemplazo"] = \
                alerta["porcentaje"]

            cambios += 1

            break

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

print(
    f"Alertas resueltas: {cambios}"
)
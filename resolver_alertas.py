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

with open(
    "estado.json",
    "r",
    encoding="utf-8"
) as f:
    estado = json.load(f)

cambios = 0

# -------------------------------------------------
# RESOLVER ALERTAS DE CONSUMIBLES
# -------------------------------------------------

for alerta in alertas["alertas"]:

    if alerta["estado"] != "notificado":
        continue

    if alerta.get("tipo") != "consumible":
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

            alerta["fecha_instalacion"] = (
                instalacion["fecha_instalacion"]
            )

            alerta["contador_instalacion"] = (
                instalacion["contador_instalacion"]
            )

            alerta["contador_total_instalacion"] = (
                instalacion.get(
                    "contador_total_instalacion",
                    instalacion["contador_instalacion"]
                )
            )

            alerta["contador_color_instalacion"] = (
                instalacion.get(
                    "contador_color_instalacion",
                    0
                )
            )

            alerta["contador_negro_instalacion"] = (
                instalacion.get(
                    "contador_negro_instalacion",
                    0
                )
            )

            alerta["porcentaje_reemplazo"] = (
                alerta["porcentaje"]
            )

            cambios += 1
            break


# -------------------------------------------------
# GUARDAR
# -------------------------------------------------

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
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

            alerta["porcentaje_reemplazo"] = (
                alerta["porcentaje"]
            )

            cambios += 1
            break

# -------------------------------------------------
# RESOLVER ALERTAS OFFLINE
# -------------------------------------------------

for alerta in alertas["alertas"]:

    if alerta.get("tipo") != "offline":
        continue

    if alerta.get("estado") != "notificado":
        continue

    equipo = next(
        (
            e
            for e in estado["impresoras"]
            if e.get("serial")
            == alerta.get("serial")
        ),
        None
    )

    if (
        equipo
        and
        equipo.get("online") is True
    ):

        alerta["estado"] = "resuelto"

        alerta["fecha_resolucion"] = (
            datetime.now().isoformat()
        )

        cambios += 1

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
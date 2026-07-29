import json
from datetime import datetime

with open(
    "metricas.json",
    "r",
    encoding="utf-8"
) as f:

    metricas = json.load(f)

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
    "instalaciones.json",
    "r",
    encoding="utf-8"
) as f:

    instalaciones = json.load(f)

with open(
    "vida_consumibles.json",
    "r",
    encoding="utf-8"
) as f:

    vida = json.load(f)

dashboard = {

    "actualizado":
        datetime.now().isoformat(),

    "metricas":
        metricas,

    "impresoras":
        estado["impresoras"],

    "alertas":
        alertas["alertas"],

    "instalaciones":
        instalaciones["instalaciones"],

    "vida_consumibles":
        vida["consumibles"]

}

with open(
    "dashboard.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        dashboard,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    "dashboard.json generado"
)

import json
from datetime import datetime

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

total = len(
    estado["impresoras"]
)

online = sum(
    1
    for i in estado["impresoras"]
    if i.get("online", False)
)

offline = total - online

alertas_abiertas = sum(
    1
    for a in alertas["alertas"]
    if a.get("estado") == "notificado"
)

alertas_criticas = sum(
    1
    for a in alertas["alertas"]
    if (
        a.get("estado") == "notificado"
        and
        a.get("criticidad") == "critico"
    )
)

alertas_advertencia = sum(
    1
    for a in alertas["alertas"]
    if (
        a.get("estado") == "notificado"
        and
        a.get("criticidad") == "advertencia"
    )
)

instalaciones_detectadas = len(
    instalaciones["instalaciones"]
)

metricas = {

    "actualizado":
        datetime.now().isoformat(),

    "impresoras": {

        "total":
            total,

        "online":
            online,

        "offline":
            offline

    },

    "alertas": {

        "abiertas":
            alertas_abiertas,

        "criticas":
            alertas_criticas,

        "advertencias":
            alertas_advertencia

    },

    "instalaciones": {

        "detectadas":
            instalaciones_detectadas

    },

    "consumibles": {

        "criticos":
            alertas_criticas,

        "advertencia":
            alertas_advertencia

    }

}

with open(
    "metricas.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metricas,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    "metricas.json generado"
)
import json
from datetime import datetime

with open(
    "estado.json",
    "r",
    encoding="utf-8"
) as f:

    estado = json.load(f)

try:

    with open(
        "historico_contadores.json",
        "r",
        encoding="utf-8"
    ) as f:

        historico = json.load(f)

except:

    historico = []

fecha = datetime.now().isoformat()

for impresora in estado.get(
    "impresoras",
    []
):

    if impresora.get(
        "contador"
    ) is None:
        continue

    historico.append({

        "fecha": fecha,

        "serial":
            impresora.get(
                "serial"
            ),

        "nombre":
            impresora.get(
                "nombre"
            ),

        "modelo":
            impresora.get(
                "modelo"
            ),

        "ip":
            impresora.get(
                "ip"
            ),

        "contador":
            impresora.get(
                "contador"
            )

    })

with open(
    "historico_contadores.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        historico,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"Registros agregados: {len(estado.get('impresoras', []))}"
)
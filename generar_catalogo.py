import json

# Abrir catálogo existente
try:

    with open(
        "catalogo_consumibles.json",
        "r",
        encoding="utf-8"
    ) as f:

        catalogo = json.load(f)

except:

    catalogo = {}

# Datos descubiertos hasta ahora
descubiertos = {

    "Xerox VersaLink B605": {

        "drum_black": "101R00582",
        "transfer": "116R00009",
        "fuser": "115R00140"

    },

    "Xerox VersaLink C9000": {

        "toner_black": "106R04085",
        "toner_yellow": "106R04084",
        "toner_magenta": "106R04083",
        "toner_cyan": "106R04082",

        "drum_black": "101R00602",
        "drum_yellow": "101R00602",
        "drum_magenta": "101R00602",
        "drum_cyan": "101R00602"

    }

}

for modelo, consumibles in descubiertos.items():

    if modelo not in catalogo:
        catalogo[modelo] = {}

    for nombre, pn in consumibles.items():

        if nombre not in catalogo[modelo]:

            catalogo[modelo][nombre] = {

                "pn": pn,
                "origen": "snmp"

            }

with open(
    "catalogo_consumibles.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        catalogo,
        f,
        indent=2,
        ensure_ascii=False
    )

print("catalogo_consumibles.json actualizado")
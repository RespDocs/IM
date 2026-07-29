from pysnmp.hlapi.v3arch.asyncio import *
import asyncio
import json
import re

COMMUNITY = "public"

MAPA_MONO = {

    1: "toner_black",

    6: "drum_black",

    10: "transfer",

    12: "fuser",

    18: "tray1_roller",

    19: "tray2_roller",

    20: "tray3_roller"

}

MAPA_COLOR = {

    1: "toner_black",
    2: "toner_yellow",
    3: "toner_magenta",
    4: "toner_cyan",

    5: "waste_toner",

    6: "drum_black",
    7: "drum_yellow",
    8: "drum_magenta",
    9: "drum_cyan",

    10: "transfer",

    12: "fuser",

    17: "belt_cleaner",

    18: "tray1_roller",

    19: "tray2_roller"

}


async def consultar(ip, oid):

    try:

        iterator = get_cmd(
            SnmpEngine(),
            CommunityData(COMMUNITY),
            await UdpTransportTarget.create(
                (ip, 161),
                timeout=2,
                retries=0
            ),
            ContextData(),
            ObjectType(
                ObjectIdentity(oid)
            )
        )

        errorIndication, errorStatus, errorIndex, varBinds = \
            await iterator

        if errorIndication:
            return None

        if errorStatus:
            return None

        return str(varBinds[0][1])

    except:
        return None


async def catalogar_modelo(ip, modelo):

    if " C" in modelo:

        mapa = MAPA_COLOR

    else:

        mapa = MAPA_MONO

    resultado = {}

    for indice, nombre in mapa.items():

        descripcion = await consultar(
            ip,
            f"1.3.6.1.2.1.43.11.1.1.6.1.{indice}"
        )

        if not descripcion:
            continue

        pn = None

        match = re.search(
            r"PN\s+([A-Z0-9]+)",
            descripcion,
            re.IGNORECASE
        )

        if match:
            pn = match.group(1)

        vida_nominal = await consultar(
            ip,
            f"1.3.6.1.2.1.43.11.1.1.8.1.{indice}"
        )

        try:

            vida_nominal = int(
                vida_nominal
            )

            if vida_nominal <= 0:
                vida_nominal = None

        except:

            vida_nominal = None

        resultado[nombre] = {

            "descripcion":
                descripcion,

            "pn":
                pn,

            "vida_nominal":
                vida_nominal,

            "origen":
                "snmp"

        }

    return resultado


async def main():

    with open(
        "impresoras.json",
        "r",
        encoding="utf-8"
    ) as f:

        inventario = json.load(f)

    representantes = {}

    for impresora in inventario["impresoras"]:

        modelo = impresora["modelo"]

        if modelo not in representantes:

            representantes[modelo] = impresora["ip"]

    catalogo = {}

    for modelo, ip in representantes.items():

        print(
            f"Catalogando {modelo}"
        )

        catalogo[modelo] = await catalogar_modelo(
            ip,
            modelo
        )

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

    print()
    print(
        "catalogo_consumibles.json generado"
    )


asyncio.run(main())
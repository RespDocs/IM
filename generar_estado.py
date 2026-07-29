import os
import shutil
from pysnmp.hlapi.v3arch.asyncio import *
import asyncio
import json
from datetime import datetime

COMMUNITY = "public"

MONO_CONSUMIBLES = {

    "toner_black": 1,
    "drum_black": 6

}

COLOR_CONSUMIBLES = {

    "toner_black": 1,
    "toner_yellow": 2,
    "toner_magenta": 3,
    "toner_cyan": 4,

    "drum_black": 6,
    "drum_yellow": 7,
    "drum_magenta": 8,
    "drum_cyan": 9

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


async def leer_consumible(ip, indice):

    actual = await consultar(
        ip,
        f"1.3.6.1.2.1.43.11.1.1.9.1.{indice}"
    )

    maximo = await consultar(
        ip,
        f"1.3.6.1.2.1.43.11.1.1.8.1.{indice}"
    )

    if actual is None:
        return None

    if maximo is None:
        return None

    try:

        actual = int(actual)
        maximo = int(maximo)

        if actual < 0:
            return None

        if maximo <= 0:
            return None

        return round(
            actual * 100 / maximo
        )

    except:
        return None


async def procesar_impresora(impresora):

    ip = impresora["ip"]

    print(
        f"Consultando {ip}"
    )

    timestamp = datetime.now().isoformat()

    contador = await consultar(
        ip,
        "1.3.6.1.2.1.43.10.2.1.4.1.1"
    )

    if contador is None:

        return {

            "nombre":
                impresora["nombre"],

            "modelo":
                impresora["modelo"],

            "serial":
                impresora["serial"],

            "ip":
                ip,

            "online":
                False,

            "ultima_lectura":
                timestamp

        }

    modelo = impresora["modelo"]

    consumibles = {}

    if (
        " C" in modelo
        or modelo.startswith(
            "Xerox VersaLink C"
        )
    ):

        tabla = COLOR_CONSUMIBLES

    else:

        tabla = MONO_CONSUMIBLES

    for nombre, indice in tabla.items():

        porcentaje = await leer_consumible(
            ip,
            indice
        )

        if porcentaje is not None:

            consumibles[
                nombre
            ] = porcentaje

    return {

        "nombre":
            impresora["nombre"],

        "modelo":
            impresora["modelo"],

        "serial":
            impresora["serial"],

        "ip":
            ip,

        "contador":
            int(contador),

        "consumibles":
            consumibles,

        "online":
            True,

        "ultima_lectura":
            timestamp

    }


async def main():

    with open(
        "impresoras.json",
        "r",
        encoding="utf-8"
    ) as f:

        inventario = json.load(f)

    resultado = []

    for impresora in inventario["impresoras"]:

        estado = await procesar_impresora(
            impresora
        )

        resultado.append(
            estado
        )

    salida = {

        "actualizado":
            datetime.now().isoformat(),

        "impresoras":
            resultado

    }

    with open(
        "estado.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            salida,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print(
        "estado.json generado"
    )


if os.path.exists(
    "estado.json"
):

    shutil.copy(
        "estado.json",
        "estado_anterior.json"
    )

asyncio.run(main())
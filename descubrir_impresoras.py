from pysnmp.hlapi.v3arch.asyncio import *
import asyncio
import json
from datetime import datetime

def expandir_rango(rango):

    inicio, fin = rango.split("-")

    base = ".".join(
        inicio.split(".")[:-1]
    )

    primer_ip = int(
        inicio.split(".")[-1]
    )

    ultima_ip = int(
        fin.split(".")[-1]
    )

    return [

        f"{base}.{i}"

        for i in range(
            primer_ip,
            ultima_ip + 1
        )

    ]


async def consultar(ip, community, oid):

    try:

        iterator = get_cmd(
            SnmpEngine(),
            CommunityData(community),
            await UdpTransportTarget.create(
                (ip, 161),
                timeout=1,
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

    except Exception:
        return None


async def main():

    with open(
        "config.json",
        "r",
        encoding="utf-8"
    ) as f:

        config = json.load(f)

    community = config["community"]

    ips = set()

    for ip in config.get(
        "listado",
        []
    ):
        ips.add(ip)

    for rango in config.get(
        "rangos",
        []
    ):

        for ip in expandir_rango(rango):
            ips.add(ip)

    print()
    print(
        f"IPs a revisar: {len(ips)}"
    )
    print()

    impresoras = []

    for ip in sorted(ips):

        print(
            f"Consultando {ip}"
        )

        modelo = await consultar(
            ip,
            community,
            "1.3.6.1.2.1.1.1.0"
        )

        if not modelo:
            continue

        if "Xerox" not in modelo:
            continue

        nombre = await consultar(
            ip,
            community,
            "1.3.6.1.2.1.1.5.0"
        )

        serial = await consultar(
            ip,
            community,
            "1.3.6.1.2.1.43.5.1.1.17.1"
        )

        impresora = {

            "nombre":
                nombre,

            "modelo":
                modelo.split(";")[0],

            "serial":
                serial,

            "ip":
                ip

        }

        impresoras.append(
            impresora
        )

        print(
            f"  Impresora encontrada: {nombre}"
        )

    salida = {

    "actualizado":
        datetime.now().isoformat(),

    "impresoras":
        impresoras

    }

    with open(
        "impresoras.json",
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
        f"Total Impresoras encontradas: {len(impresoras)}"
    )

    print(
        "impresoras.json generado"
    )


asyncio.run(main())
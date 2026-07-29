from pysnmp.hlapi.v3arch.asyncio import *
import asyncio

IP = "172.16.79.199"
COMMUNITY = "public"


async def consultar_oid(oid):

    iterator = get_cmd(
        SnmpEngine(),
        CommunityData(COMMUNITY),
        await UdpTransportTarget.create(
            (IP, 161)
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


async def main():

    modelo = await consultar_oid(
        "1.3.6.1.2.1.1.1.0"
    )

    nombre = await consultar_oid(
        "1.3.6.1.2.1.1.5.0"
    )

    serial = await consultar_oid(
        "1.3.6.1.2.1.43.5.1.1.17.1"
    )

    contador = await consultar_oid(
        "1.3.6.1.2.1.43.10.2.1.4.1.1"
    )

    toner_actual = int(
        await consultar_oid(
            "1.3.6.1.2.1.43.11.1.1.9.1.1"
        )
    )

    toner_max = int(
        await consultar_oid(
            "1.3.6.1.2.1.43.11.1.1.8.1.1"
        )
    )

    drum_actual = int(
        await consultar_oid(
            "1.3.6.1.2.1.43.11.1.1.9.1.6"
        )
    )

    drum_max = int(
        await consultar_oid(
            "1.3.6.1.2.1.43.11.1.1.8.1.6"
        )
    )

    toner_pct = round(
        toner_actual * 100 / toner_max
    )

    drum_pct = round(
        drum_actual * 100 / drum_max
    )

    print()
    print("=" * 50)
    print("XEROX MONITOR")
    print("=" * 50)

    print(f"Nombre       : {nombre}")
    print(f"Modelo       : {modelo}")
    print(f"Serial       : {serial}")
    print(f"IP           : {IP}")

    print()

    print(f"Contador     : {contador}")

    print()

    print(f"Toner Negro  : {toner_pct}%")
    print(f"Drum         : {drum_pct}%")

    print()
    print("=" * 50)


asyncio.run(main())
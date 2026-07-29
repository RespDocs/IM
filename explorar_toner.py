from pysnmp.hlapi.v3arch.asyncio import *
import asyncio

IP = "172.16.79.199"
COMMUNITY = "public"

async def consultar(oid):

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

    for oid in [

        "1.3.6.1.2.1.43.11.1.1.2.1.1",
        "1.3.6.1.2.1.43.11.1.1.5.1.1",
        "1.3.6.1.2.1.43.11.1.1.6.1.1",
        "1.3.6.1.2.1.43.11.1.1.7.1.1",
        "1.3.6.1.2.1.43.11.1.1.8.1.1",
        "1.3.6.1.2.1.43.11.1.1.9.1.1"

    ]:

        valor = await consultar(oid)

        print()
        print(oid)
        print(valor)

asyncio.run(main())
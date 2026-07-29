from pysnmp.hlapi.asyncio import *
import asyncio

async def main():

    transport = await UdpTransportTarget.create(
        ("172.16.79.199", 161)
    )

    iterator = next_cmd(
        SnmpEngine(),
        CommunityData("public"),
        transport,
        ContextData(),
        ObjectType(
            ObjectIdentity(
                "1.3.6.1.2.1.43.11.1.1.6"
            )
        ),
        lexicographicMode=False
    )

    async for (
        errorIndication,
        errorStatus,
        errorIndex,
        varBinds
    ) in iterator:

        if errorIndication:
            print(errorIndication)
            break

        if errorStatus:
            print(errorStatus.prettyPrint())
            break

        for varBind in varBinds:
            print(varBind)

asyncio.run(main())
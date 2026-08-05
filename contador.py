from pysnmp.hlapi.v3arch.asyncio import *
import asyncio


async def consultar():

    iterator = get_cmd(
        SnmpEngine(),
        CommunityData("public"),
        await UdpTransportTarget.create(
            ("172.16.79.73", 161)
        ),
        ContextData(),
        ObjectType(
            ObjectIdentity(
                "1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33"
            )
        )
    )

    errorIndication, errorStatus, errorIndex, varBinds = \
        await iterator

    if errorIndication:
        print(errorIndication)
        return

    if errorStatus:
        print(errorStatus.prettyPrint())
        return

    for varBind in varBinds:
        print(varBind)

asyncio.run(consultar())
from pysnmp.hlapi.v3arch.asyncio import *
import asyncio

async def main():

    iterator = get_cmd(
        SnmpEngine(),
        CommunityData("public"),
        await UdpTransportTarget.create(
            ("172.16.79.199", 161)
        ),
        ContextData(),
        ObjectType(
            ObjectIdentity(
                "1.3.6.1.2.1.43.11.1.1.9.1.18"
            )
        )
    )

    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    for varBind in varBinds:
        print(varBind)

asyncio.run(main()) 
from pysnmp.hlapi.v3arch.asyncio import *
import asyncio

async def main():

    for indice in range(1, 20):

        try:

            iterator = get_cmd(
                SnmpEngine(),
                CommunityData("public"),
                await UdpTransportTarget.create(
                    ("172.16.79.28", 161)
                ),
                ContextData(),
                ObjectType(
                    ObjectIdentity(
                        f"1.3.6.1.2.1.43.11.1.1.6.1.{indice}"
                    )
                )
            )

            errorIndication, errorStatus, errorIndex, varBinds = await iterator

            if errorIndication:
                continue

            if errorStatus:
                continue

            for varBind in varBinds:

                valor = str(varBind[1])

                if valor:
                    print(
                        f"Indice {indice}: {valor}"
                    )

        except Exception:
            pass

asyncio.run(main())
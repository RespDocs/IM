from pysnmp.hlapi import *

ip = "172.16.79.28"

for (
    errorIndication,
    errorStatus,
    errorIndex,
    varBinds
) in nextCmd(

    SnmpEngine(),
    CommunityData("public"),
    UdpTransportTarget((ip, 161)),
    ContextData(),
    ObjectType(
        ObjectIdentity(
            "1.3.6.1.2.1.43"
        )
    ),
    lexicographicMode=False

):

    if errorIndication:
        print(errorIndication)
        break

    if errorStatus:
        print(errorStatus.prettyPrint())
        break

    for varBind in varBinds:
        print(varBind)
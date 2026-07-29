import json
from datetime import datetime


def cargar(nombre):

    try:

        with open(
            nombre,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}


metricas = cargar(
    "metricas.json"
)

estado = cargar(
    "estado.json"
)

alertas = cargar(
    "alertas.json"
)

instalaciones = cargar(
    "instalaciones.json"
)

vida = cargar(
    "vida_consumibles.json"
)

catalogo = cargar(
    "catalogo_consumibles.json"
)

inventario = cargar(
    "inventario_detalle.json"
)


# -------------------------------------------------
# INVENTARIO
# -------------------------------------------------

for impresora in estado.get(
    "impresoras",
    []
):

    serial = impresora.get(
        "serial"
    )

    if serial in inventario:

        impresora.update(
            inventario[serial]
        )


# -------------------------------------------------
# ALERTAS ENRIQUECIDAS
# -------------------------------------------------

alertas_dashboard = []

for alerta in alertas.get(
    "alertas",
    []
):

    equipo = next(

        (
            i
            for i in estado.get(
                "impresoras",
                []
            )
            if i["nombre"]
            == alerta["equipo"]
        ),

        None

    )

    serial = None
    modelo = None
    pn = None

    if equipo:

        serial = equipo.get(
            "serial"
        )

        modelo = equipo.get(
            "modelo"
        )

        if (

            modelo in catalogo

            and

            alerta.get(
                "consumible"
            )

            in catalogo[
                modelo
            ]

        ):

            pn = catalogo[
                modelo
            ][
                alerta[
                    "consumible"
                ]
            ].get(
                "pn"
            )

    alerta_dashboard = {

        **alerta,

        "serial":
            serial,

        "modelo":
            modelo,

        "pn":
            pn

    }

    alertas_dashboard.append(
        alerta_dashboard
    )


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

dashboard = {

    "actualizado":
        datetime.now().isoformat(),

    "metricas":
        metricas,

    "impresoras":
        estado.get(
            "impresoras",
            []
        ),

    "alertas":
        alertas_dashboard,

    "instalaciones":
        instalaciones.get(
            "instalaciones",
            []
        ),

    "vida_consumibles":
        vida.get(
            "consumibles",
            []
        )

}

with open(

    "dashboard.json",

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        dashboard,

        f,

        indent=2,

        ensure_ascii=False

    )

print(
    "dashboard.json generado"
)
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path


ARCHIVO_CONTROL = "control_monitor.json"


def ejecutar(script):

    print()
    print("=" * 60)
    print(f"Ejecutando: {script}")
    print("=" * 60)

    resultado = subprocess.run(
        ["python", script],
        capture_output=True,
        text=True
    )

    if resultado.stdout:
        print(resultado.stdout)

    if resultado.stderr:
        print("ERRORES:")
        print(resultado.stderr)


def cargar_control():

    if not Path(
        ARCHIVO_CONTROL
    ).exists():

        return {
            "ultima_ejecucion_descubrimiento":
                None
        }

    with open(
        ARCHIVO_CONTROL,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def guardar_control(control):

    with open(
        ARCHIVO_CONTROL,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            control,
            f,
            indent=2,
            ensure_ascii=False
        )


while True:

    print()
    print("=" * 60)
    print("IMPRESORAS MONITOR")
    print(
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    print("=" * 60)

    with open(
        "config_monitor.json",
        "r",
        encoding="utf-8"
    ) as f:

        config = json.load(f)

    control = cargar_control()

    ahora = datetime.now()

    ejecutar_descubrimiento = False

    if (
        control[
            "ultima_ejecucion_descubrimiento"
        ] is None
    ):

        ejecutar_descubrimiento = True

    else:

        ultima = datetime.fromisoformat(

            control[
                "ultima_ejecucion_descubrimiento"
            ]

        )

        horas = (
            ahora - ultima
        ).total_seconds() / 3600

        if horas >= config[
            "descubrimiento_cada_horas"
        ]:

            ejecutar_descubrimiento = True

    if ejecutar_descubrimiento:

        ejecutar(
            "descubrir_impresoras.py"
        )

        ejecutar(
            "catalogar_consumibles.py"
        )

        control[
            "ultima_ejecucion_descubrimiento"
        ] = ahora.isoformat()

        guardar_control(
            control
        )

    ejecutar("generar_estado.py")

    ejecutar("detectar_alertas.py")

    ejecutar(
        "detectar_instalaciones.py"
    )

    ejecutar(
        "resolver_alertas.py"
    )

    ejecutar(
        "calcular_vida.py"
    )

    ejecutar(
        "generar_metricas.py"
    )

    minutos = config[
        "intervalo_minutos"
    ]

    print()
    print(
        f"Próxima ejecución en "
        f"{minutos} minutos"
    )

    time.sleep(
        minutos * 60
    )
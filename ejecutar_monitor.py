import subprocess
from datetime import datetime


def ejecutar(script):

    print()
    print("=" * 60)
    print(f"Ejecutando {script}")
    print("=" * 60)

    resultado = subprocess.run(
        ["python", script],
        capture_output=True,
        text=True
    )

    print(resultado.stdout)

    if resultado.stderr:

        print("ERRORES:")

        print(resultado.stderr)


print()
print("=" * 60)
print("IMPRESORAS MONITOR")
print(
    datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
)
print("=" * 60)

ejecutar("descubrir_impresoras.py")

ejecutar("generar_estado.py")

ejecutar("catalogar_consumibles.py")

ejecutar("detectar_alertas.py")

ejecutar("detectar_instalaciones.py")

ejecutar("resolver_alertas.py")

ejecutar("calcular_vida.py")

ejecutar("generar_metricas.py")

print()
print("=" * 60)
print("PROCESO FINALIZADO")
print("=" * 60)
import subprocess
from datetime import datetime

GIT = r"C:\Program Files\Git\cmd\git.exe"


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

    if resultado.stdout:
        print(resultado.stdout)

    if resultado.stderr:
        print("ERRORES:")
        print(resultado.stderr)


def publicar_github():

    print()
    print("=" * 60)
    print("PUBLICANDO EN GITHUB")
    print("=" * 60)

    try:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        subprocess.run(
            [GIT, "add", "."],
            check=True
        )

        commit = subprocess.run(
            [
                GIT,
                "commit",
                "-m",
                f"Actualizacion {timestamp}"
            ],
            capture_output=True,
            text=True
        )

        print(commit.stdout)

        push = subprocess.run(
            [GIT, "push"],
            capture_output=True,
            text=True
        )

        print(push.stdout)

        if push.stderr:
            print(push.stderr)

        print()
        print(
            "✅ Dashboard publicado correctamente"
        )

    except Exception as e:

        print()
        print(
            f"❌ Error publicando en GitHub: {e}"
        )


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

ejecutar("generar_dashboard_json.py")

publicar_github()

print()
print("=" * 60)
print("PROCESO FINALIZADO")
print("=" * 60)
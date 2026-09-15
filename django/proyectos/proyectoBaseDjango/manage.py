import os
import sys


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "config.settings.development",
    )

    try:
        from django.core.management import (
            execute_from_command_line,
        )

    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. "
            "Comprueba que Django esté instalado "
            "y que el entorno virtual esté activado."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

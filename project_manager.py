import json
from pathlib import Path


class ProjectManager:
    """
    Gestiona la carga, guardado y validación
    de proyectos TSB.
    """
    SUPPORTED_VERSIONS = [
    "1.1"]

    @classmethod
    def is_supported_version(
        cls,
        project_data
    ):

        version = project_data.get(
            "version"
        )

        return (
            version
            in cls.SUPPORTED_VERSIONS
        )

    PROJECT_VERSION = "1.1"

    @classmethod
    def save_project(
        cls,
        filepath,
        project_name,
        sound_files
    ):
        """
        Funcionamiento:
        Guarda un proyecto TSB.

        Entradas:
        - filepath (str): Ruta destino.
        - project_name (str): Nombre del proyecto.
        - sound_files (dict): Diccionario de sonidos.

        Salidas:
        - success (bool): True si se guardó.
        """

        try:

            data = {

                "version":
                cls.PROJECT_VERSION,

                "project_name":
                project_name,

                "files":
                sound_files
            }

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except Exception:

            return False

    @classmethod
    def load_project(
        cls,
        filepath
    ):
        """
        Funcionamiento:
        Carga un proyecto TSB.

        Entradas:
        - filepath (str): Ruta del proyecto.

        Salidas:
        - project_data (dict | None)
        """

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return None

    @staticmethod
    def validate_project(
        project_data
    ):
        """
        Funcionamiento:
        Comprueba que la estructura
        básica del proyecto sea válida.

        Entradas:
        - project_data (dict)

        Salidas:
        - valid (bool)
        """

        required_keys = [

            "version",
            "project_name",
            "files"
        ]

        return all(
            key in project_data
            for key in required_keys
        )

    @staticmethod
    def validate_files(
        sound_files
    ):
        """
        Funcionamiento:
        Verifica qué archivos del proyecto
        siguen existiendo.

        Entradas:
        - sound_files (dict)

        Salidas:
        - validation (dict)
        """

        validation = {}

        for sound_name, filepath in sound_files.items():

            if not filepath:

                validation[sound_name] = False

                continue

            validation[sound_name] = (
                Path(filepath).exists()
            )

        return validation

    @staticmethod
    def get_missing_files(
        sound_files
    ):
        """
        Funcionamiento:
        Devuelve una lista con los sonidos
        cuyos archivos ya no existen.

        Entradas:
        - sound_files (dict)

        Salidas:
        - missing_files (list)
        """

        missing_files = []

        for sound_name, filepath in sound_files.items():

            if not filepath:

                continue

            if not Path(filepath).exists():

                missing_files.append(
                    sound_name
                )

        return missing_files

    @staticmethod
    def project_exists(
        filepath
    ):
        """
        Funcionamiento:
        Verifica si un proyecto existe.

        Entradas:
        - filepath (str)

        Salidas:
        - exists (bool)
        """

        return Path(
            filepath
        ).exists()

    @staticmethod
    def get_project_version(
        project_data
    ):
        """
        Funcionamiento:
        Obtiene la versión de un proyecto.

        Entradas:
        - project_data (dict)

        Salidas:
        - version (str)
        """

        return project_data.get(
            "version",
            "unknown"
        )
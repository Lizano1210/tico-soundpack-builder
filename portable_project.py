# portable_project.py

import json
import shutil
import tempfile
import zipfile
from pathlib import Path


PORTABLE_VERSION = "1.2"


class PortableProjectManager:

    # ==================================================
    # EXPORTACIÓN
    # ==================================================

    @staticmethod
    def export(
        destination_path,
        project_name,
        sound_files
    ):
        """
        Empaqueta el proyecto y todos sus archivos
        de audio en un .tsbz.
        """

        with tempfile.TemporaryDirectory() as tmp_dir:

            tmp_path = Path(tmp_dir)

            project_json = {
                "version": PORTABLE_VERSION,
                "project_name": project_name,
                "files": {}
            }

            for sound_name, value in sound_files.items():

                if isinstance(value, dict):

                    main = value.get("main")
                    extras = value.get("extras", [])

                    if not main:
                        continue

                    main_filename = Path(main).name

                    shutil.copy2(main, tmp_path / main_filename)

                    exported_extras = []

                    for extra in extras:

                        path = extra.get("path")
                        name = extra.get("name")

                        if not path or not Path(path).exists():
                            continue

                        extra_filename = Path(path).name

                        shutil.copy2(
                            path,
                            tmp_path / extra_filename
                        )

                        exported_extras.append(
                            {
                                "name": name,
                                "path": extra_filename
                            }
                        )

                    project_json["files"][sound_name] = {
                        "main": main_filename,
                        "extras": exported_extras
                    }

                else:

                    if not value or not Path(value).exists():
                        continue

                    filename = Path(value).name

                    shutil.copy2(value, tmp_path / filename)

                    project_json["files"][sound_name] = filename

            # Guardar project.json

            with open(
                tmp_path / "project.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(project_json, f, indent=4)

            # Comprimir como .tsbz

            with zipfile.ZipFile(
                destination_path,
                "w",
                zipfile.ZIP_DEFLATED
            ) as zf:

                for file in tmp_path.iterdir():

                    if file.is_file():
                        zf.write(file, arcname=file.name)

        return destination_path

    # ==================================================
    # IMPORTACIÓN
    # ==================================================

    @staticmethod
    def import_project(
        tsbz_path
    ):
        """
        Extrae el .tsbz a una carpeta temporal y
        reconstruye la estructura del proyecto.

        Retorna:
        - (project_data, tmp_dir) si es válido.
        - None si falta project.json.

        El llamador es responsable de limpiar tmp_dir
        cuando el proyecto ya no esté en uso.
        """

        tmp_dir = tempfile.mkdtemp()
        tmp_path = Path(tmp_dir)

        with zipfile.ZipFile(tsbz_path, "r") as zf:
            zf.extractall(tmp_path)

        project_json_path = tmp_path / "project.json"

        if not project_json_path.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)
            return None

        with open(
            project_json_path,
            "r",
            encoding="utf-8"
        ) as f:
            project_data = json.load(f)

        # Resolver rutas relativas a absolutas

        resolved_files = {}

        for sound_name, value in project_data.get(
            "files", {}
        ).items():

            if isinstance(value, dict):

                main_filename = value.get("main")
                main_path = tmp_path / main_filename if main_filename else None

                resolved_extras = []

                for extra in value.get("extras", []):

                    extra_path = tmp_path / extra["path"]

                    resolved_extras.append(
                        {
                            "name": extra["name"],
                            "path": str(extra_path)
                        }
                    )

                resolved_files[sound_name] = {
                    "main": str(main_path) if main_path else None,
                    "extras": resolved_extras
                }

            else:

                file_path = tmp_path / value if value else None

                resolved_files[sound_name] = (
                    str(file_path) if file_path else None
                )

        return {
            "project_name": project_data.get(
                "project_name", ""
            ),
            "files": resolved_files,
            "tmp_dir": tmp_dir
        }

    # ==================================================
    # GUARDAR COMO LOCAL
    # ==================================================

    @staticmethod
    def save_as_local(
        destination_folder,
        project_name,
        sound_files
    ):
        """
        Copia todos los archivos a una carpeta local
        y genera un .tsbp con rutas absolutas.
        Usado cuando el usuario guarda un proyecto
        portable como proyecto local.
        """

        project_folder = Path(destination_folder) / project_name

        project_folder.mkdir(parents=True, exist_ok=True)

        local_files = {}

        for sound_name, value in sound_files.items():

            if isinstance(value, dict):

                main = value.get("main")
                local_extras = []

                if main and Path(main).exists():

                    dest = project_folder / Path(main).name
                    shutil.copy2(main, dest)
                    local_main = str(dest)

                else:

                    local_main = None

                for extra in value.get("extras", []):

                    path = extra.get("path")

                    if path and Path(path).exists():

                        dest = project_folder / Path(path).name
                        shutil.copy2(path, dest)

                        local_extras.append(
                            {
                                "name": extra["name"],
                                "path": str(dest)
                            }
                        )

                local_files[sound_name] = {
                    "main": local_main,
                    "extras": local_extras
                }

            else:

                if value and Path(value).exists():

                    dest = project_folder / Path(value).name
                    shutil.copy2(value, dest)
                    local_files[sound_name] = str(dest)

                else:

                    local_files[sound_name] = None

        return local_files, project_folder
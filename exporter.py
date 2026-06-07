import zipfile
from pathlib import Path
import shutil
from pathlib import Path
import shutil


class SoundpackExporter:

    @staticmethod
    def create_zip(soundpack_path):

        zip_path = soundpack_path.with_suffix(".zip")

        with zipfile.ZipFile(
            zip_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for file in soundpack_path.rglob("*"):

                if file.is_file():

                    zip_file.write(
                        file,
                        arcname=file.relative_to(soundpack_path)
                    )

        return zip_path

    @staticmethod
    def create_soundpack(
        destination_folder,
        soundpack_name,
        sound_files,
        formats
    ):

        soundpack_path = Path(destination_folder) / soundpack_name

        soundpack_path.mkdir(parents=True, exist_ok=True)

        for sound_name, value in sound_files.items():

            fmt = formats[sound_name]
            has_folders = isinstance(fmt, dict) and fmt.get("folders")

            if has_folders and isinstance(value, dict):

                main = value.get("main")

                if main:
                    extension = Path(main).suffix
                    shutil.copy2(
                        main,
                        soundpack_path / f"{sound_name}{extension}"
                    )

                for extra in value.get("extras", []):

                    path = extra.get("path")
                    name = extra.get("name")

                    if not path or not name:
                        continue

                    extra_folder = (
                        soundpack_path / "songs" / name
                    )

                    extra_folder.mkdir(parents=True, exist_ok=True)

                    extension = Path(path).suffix

                    shutil.copy2(
                        path,
                        extra_folder / f"{sound_name}{extension}"
                    )

            else:

                if not value:
                    continue

                extension = Path(value).suffix

                shutil.copy2(
                    value,
                    soundpack_path / f"{sound_name}{extension}"
                )

        return soundpack_path
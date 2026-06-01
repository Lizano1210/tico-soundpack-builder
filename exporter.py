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

            for file in soundpack_path.iterdir():

                zip_file.write(
                    file,
                    arcname=file.name
                )

        return zip_path

    @staticmethod
    def create_soundpack(
        destination_folder,
        soundpack_name,
        sound_files
    ):

        soundpack_path = (
            Path(destination_folder)
            / soundpack_name
        )

        soundpack_path.mkdir(
            parents=True,
            exist_ok=True
        )

        for sound_name, source_file in sound_files.items():

            extension = Path(source_file).suffix

            destination_file = (
                soundpack_path
                / f"{sound_name}{extension}"
            )

            shutil.copy2(
                source_file,
                destination_file
            )

        return soundpack_path
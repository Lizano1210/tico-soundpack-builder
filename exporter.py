import zipfile
from pathlib import Path
import shutil
from pathlib import Path
import shutil
from ffmpeg_manager import FFmpegManager


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

            if isinstance(fmt, dict):
                target_format = fmt["format"]
                has_folders = fmt.get("folders", False)
            else:
                target_format = fmt
                has_folders = False

            if has_folders and isinstance(value, dict):

                main = value.get("main")

                if main:

                    output_path = (
                        soundpack_path
                        / f"{sound_name}.{target_format}"
                    )

                    FFmpegManager.prepare_audio_for_export(
                        main,
                        target_format,
                        output_path
                    )

                for extra in value.get("extras", []):

                    path = extra.get("path")
                    name = extra.get("name")

                    if not path or not name:
                        continue

                    extra_folder = (
                        soundpack_path / "songs" / name
                    )

                    extra_folder.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    output_path = (
                        extra_folder
                        / f"{sound_name}.{target_format}"
                    )

                    FFmpegManager.prepare_audio_for_export(
                        path,
                        target_format,
                        output_path
                    )

            else:

                if not value:
                    continue

                output_path = (
                    soundpack_path
                    / f"{sound_name}.{target_format}"
                )

                FFmpegManager.prepare_audio_for_export(
                    value,
                    target_format,
                    output_path
                )

        return soundpack_path
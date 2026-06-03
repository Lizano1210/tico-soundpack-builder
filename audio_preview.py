# audio_preview.py

import json
import subprocess

from ffmpeg_manager import FFmpegManager


class AudioPreview:
    """
    Gestiona la reproducción y análisis
    de archivos de audio mediante FFmpeg.
    """

    def __init__(self):

        self.current_process = None

        self.ffplay_path = (
            FFmpegManager.get_ffplay_path()
        )

        self.ffprobe_path = (
            FFmpegManager.get_ffprobe_path()
        )
        self.current_file = None

    def play(self, filepath):
        """
        Funcionamiento:
        Reproduce un archivo de audio.

        Entradas:
        - filepath (str): Ruta del audio.

        Salidas:
        - Ninguna.
        """

        self.stop()

        self.current_process = subprocess.Popen(
            [
                self.ffplay_path,
                "-nodisp",
                "-autoexit",
                filepath
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.current_file = filepath

    def stop(self):
        """
        Funcionamiento:
        Detiene la reproducción actual.

        Entradas:
        - Ninguna.

        Salidas:
        - Ninguna.
        """

        if self.current_process:

            if self.is_playing():

                self.current_process.terminate()

            self.current_process = None

        self.current_file = None
    
    def cleanup(self):
        """
        Funcionamiento:
        Libera recursos y detiene cualquier
        reproducción activa antes de cerrar
        la aplicación.

        Entradas:
        - Ninguna.

        Salidas:
        - Ninguna.
        """

        self.stop()

    def is_playing(self):
        """
        Funcionamiento:
        Indica si existe un audio reproduciéndose.

        Entradas:
        - Ninguna.

        Salidas:
        - playing (bool)
        """

        if not self.current_process:
            return False

        return (
            self.current_process.poll()
            is None
        )

    def get_file_info(self, filepath):
        """
        Funcionamiento:
        Obtiene metadata básica de un audio.

        Entradas:
        - filepath (str)

        Salidas:
        - info (dict)
        """

        try:

            result = subprocess.run(
                [
                    self.ffprobe_path,
                    "-v",
                    "quiet",
                    "-print_format",
                    "json",
                    "-show_format",
                    "-show_streams",
                    filepath
                ],
                capture_output=True,
                text=True
            )

            data = json.loads(
                result.stdout
            )

            audio_stream = (
                data["streams"][0]
            )

            return {

                "duration": float(
                    data["format"].get(
                        "duration",
                        0
                    )
                ),

                "bitrate": int(
                    data["format"].get(
                        "bit_rate",
                        0
                    )
                ),

                "codec": audio_stream.get(
                    "codec_name",
                    "unknown"
                ),

                "channels": audio_stream.get(
                    "channels",
                    0
                ),

                "sample_rate": int(
                    audio_stream.get(
                        "sample_rate",
                        0
                    )
                )
            }

        except Exception:

            return None

    def get_duration(self, filepath):
        """
        Funcionamiento:
        Obtiene la duración de un audio.

        Entradas:
        - filepath (str)

        Salidas:
        - duration (float | None)
        """

        info = self.get_file_info(
            filepath
        )

        if not info:
            return None

        return info["duration"]

    def format_duration(self, filepath):
        """
        Funcionamiento:
        Devuelve la duración en MM:SS.

        Entradas:
        - filepath (str)

        Salidas:
        - formatted_duration (str)
        """

        duration = (
            self.get_duration(
                filepath
            )
        )

        if duration is None:

            return "--:--"

        minutes = int(
            duration // 60
        )

        seconds = int(
            duration % 60
        )

        return (
            f"{minutes:02}:{seconds:02}"
        )
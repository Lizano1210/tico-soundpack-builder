# ffmpeg_manager.py

from pathlib import Path
import platform


class FFmpegManager:
    """
    Gestiona las rutas de FFmpeg,
    FFplay y FFprobe para todas
    las plataformas soportadas.
    """

    @staticmethod
    def _get_binary_name(binary_name):
        """
        Funcionamiento:
        Obtiene el nombre correcto del
        ejecutable según el sistema operativo.

        Entradas:
        - binary_name (str): Nombre base del ejecutable.

        Salidas:
        - executable_name (str): Nombre final del ejecutable.
        """

        if platform.system() == "Windows":
            return f"{binary_name}.exe"

        return binary_name

    @classmethod
    def _get_binary_path(cls, binary_name):
        """
        Funcionamiento:
        Obtiene la ruta absoluta hacia
        un ejecutable de FFmpeg.

        Entradas:
        - binary_name (str): ffmpeg, ffplay o ffprobe.

        Salidas:
        - binary_path (Path): Ruta al ejecutable.
        """

        executable = cls._get_binary_name(
            binary_name
        )

        return (
            Path(__file__).parent
            / "ffmpeg"
            / executable
        )

    @classmethod
    def get_ffmpeg_path(cls):
        """
        Funcionamiento:
        Obtiene la ruta de ffmpeg.

        Entradas:
        - Ninguna.

        Salidas:
        - ffmpeg_path (str): Ruta del ejecutable.
        """

        return str(
            cls._get_binary_path("ffmpeg")
        )

    @classmethod
    def get_ffplay_path(cls):
        """
        Funcionamiento:
        Obtiene la ruta de ffplay.

        Entradas:
        - Ninguna.

        Salidas:
        - ffplay_path (str): Ruta del ejecutable.
        """

        return str(
            cls._get_binary_path("ffplay")
        )

    @classmethod
    def get_ffprobe_path(cls):
        """
        Funcionamiento:
        Obtiene la ruta de ffprobe.

        Entradas:
        - Ninguna.

        Salidas:
        - ffprobe_path (str): Ruta del ejecutable.
        """

        return str(
            cls._get_binary_path("ffprobe")
        )

    @classmethod
    def ffmpeg_exists(cls):
        """
        Funcionamiento:
        Verifica si ffmpeg está disponible.

        Entradas:
        - Ninguna.

        Salidas:
        - exists (bool): True si existe.
        """

        return Path(
            cls.get_ffmpeg_path()
        ).exists()

    @classmethod
    def ffplay_exists(cls):
        """
        Funcionamiento:
        Verifica si ffplay está disponible.

        Entradas:
        - Ninguna.

        Salidas:
        - exists (bool): True si existe.
        """

        return Path(
            cls.get_ffplay_path()
        ).exists()

    @classmethod
    def ffprobe_exists(cls):
        """
        Funcionamiento:
        Verifica si ffprobe está disponible.

        Entradas:
        - Ninguna.

        Salidas:
        - exists (bool): True si existe.
        """

        return Path(
            cls.get_ffprobe_path()
        ).exists()

    @classmethod
    def validate_installation(cls):
        """
        Funcionamiento:
        Comprueba que todas las herramientas
        necesarias de FFmpeg existan.

        Entradas:
        - Ninguna.

        Salidas:
        - valid (bool): True si todo está correcto.
        """

        return all(
            [
                cls.ffmpeg_exists(),
                cls.ffplay_exists(),
                cls.ffprobe_exists()
            ]
        )
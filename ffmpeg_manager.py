# ffmpeg_manager.py

from pathlib import Path
import platform
import sys
import shutil
import platform
from pathlib import Path


class FFmpegManager:
    """
    Gestiona las rutas de FFmpeg,
    FFplay y FFprobe para todas
    las plataformas soportadas.
    """

    @staticmethod
    def _get_binary_name(binary_name):
        if platform.system() == "Windows":
            return f"{binary_name}.exe"
        return binary_name

    @classmethod
    def _get_binary_path(cls, binary_name):
        executable = cls._get_binary_name(binary_name)
        
        # Resuelve la base igual que resource_path
        base = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
        bundled = base / "ffmpeg" / executable
        
        if bundled.exists():
            return bundled
        
        # Fallback al PATH del sistema
        system_path = shutil.which(binary_name)
        if system_path:
            return Path(system_path)
        
        return bundled

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
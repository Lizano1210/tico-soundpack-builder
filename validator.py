from pathlib import Path


class SoundValidator:

    SUPPORTED_AUDIO_EXTENSIONS = {
        ".mp3", ".wav", ".flac", ".ogg",
        ".opus", ".m4a", ".aac", ".wma"
    }

    @staticmethod
    def validate_extension(
        filepath,
        expected_extension
    ):

        extension = Path(filepath).suffix.lower()

        return extension == f".{expected_extension}"
    
    @staticmethod
    def is_supported_audio(filepath):
        """
        Verifica que el archivo tenga una
        extensión de audio compatible.
        """

        return (
            Path(filepath).suffix.lower()
            in SoundValidator.SUPPORTED_AUDIO_EXTENSIONS
        )
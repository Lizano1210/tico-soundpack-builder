from pathlib import Path


class SoundValidator:

    @staticmethod
    def validate_extension(
        filepath,
        expected_extension
    ):

        extension = Path(filepath).suffix.lower()

        return extension == f".{expected_extension}"
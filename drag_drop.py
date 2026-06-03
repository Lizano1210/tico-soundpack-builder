from pathlib import Path

from tkinterdnd2 import (
    DND_FILES
)


class DragDropManager:
    """
    Gestiona zonas de drag and drop.
    """

    def __init__(self):

        self.targets = {}

    @staticmethod
    def validate_extension(
        sound_name,
        filepath
    ):
        """
        Funcionamiento:
        Valida la extensión permitida.

        Entradas:
        - sound_name (str)
        - filepath (str)

        Salidas:
        - valid (bool)
        """

        extension = (
            Path(filepath)
            .suffix
            .lower()
        )

        if sound_name == (
            "background_music"
        ):

            return (
                extension == ".opus"
            )

        return (
            extension == ".mp3"
        )

    def register_target(
        self,
        widget,
        sound_name,
        callback
    ):
        """
        Funcionamiento:
        Registra una zona de drop.

        Entradas:
        - widget
        - sound_name (str)
        - callback (function)

        Salidas:
        - Ninguna.
        """

        widget.drop_target_register(
            DND_FILES
        )

        widget.dnd_bind(
            "<<Drop>>",
            lambda event:
            self._handle_drop(
                event,
                sound_name,
                callback
            )
        )

    def _handle_drop(
        self,
        event,
        sound_name,
        callback
    ):
        """
        Procesa un archivo soltado.
        """

        filepath = (
            event.data
            .strip("{}")
        )

        if not self.validate_extension(
            sound_name,
            filepath
        ):
            return

        callback(
            sound_name,
            filepath
        )
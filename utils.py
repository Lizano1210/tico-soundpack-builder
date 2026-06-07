import sys
from pathlib import Path
from pathlib import Path
from language import LANGUAGES

def resource_path(relative_path):
    """Resuelve rutas tanto en desarrollo como en el ejecutable."""
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
    return base / relative_path

def get_current_file(self):

    return self.current_file

def assign_file(
        app,
        sound_name,
        filepath
    ):
        resource = app.sound_files[sound_name]

        if isinstance(resource, dict):
            app.sound_files[sound_name]["main"] = filepath
        else:
            app.sound_files[sound_name] = filepath

        filename = Path(filepath).name

        app.file_labels[sound_name].configure(
            text=f"✅ {filename}"
        )

        app.select_buttons[sound_name].configure(
            text=LANGUAGES[app.current_language]["change_file"]
        )


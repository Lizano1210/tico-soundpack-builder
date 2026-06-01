import sys
from pathlib import Path

def resource_path(relative_path):
    """Resuelve rutas tanto en desarrollo como en el ejecutable."""
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
    return base / relative_path
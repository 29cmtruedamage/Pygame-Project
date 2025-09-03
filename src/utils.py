# src/utils.py
import sys, os

def resource_path(relative_path: str) -> str:
    """Gibt den richtigen Pfad zurück, egal ob dev oder .app"""
    if hasattr(sys, "_MEIPASS"):  # wenn pyinstaller läuft
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

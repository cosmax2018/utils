from __future__ import annotations

import os
from pathlib import Path


APP_NAME = "QRGenerator"


def data_directory() -> Path:
    """Restituisce una cartella utente sempre scrivibile."""
    base = os.getenv("LOCALAPPDATA")
    root = Path(base) if base else Path.home() / ".local" / "share"
    folder = root / APP_NAME
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def database_path() -> Path:
    return data_directory() / "qrgenerator.db"


def log_path() -> Path:
    return data_directory() / "qrgenerator.log"

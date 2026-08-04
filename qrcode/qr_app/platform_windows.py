from __future__ import annotations

import io
import os
import tempfile

from PIL import Image


def copy_image(image: Image.Image) -> None:
    try:
        import win32clipboard
    except ImportError as exc:
        raise RuntimeError("Per la clipboard installare pywin32") from exc

    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    finally:
        win32clipboard.CloseClipboard()


def print_image(image: Image.Image) -> None:
    if os.name != "nt":
        raise RuntimeError("La stampa diretta e disponibile solo su Windows")
    filename = os.path.join(tempfile.gettempdir(), "qr_label_print.png")
    image.save(filename)
    os.startfile(filename, "print")

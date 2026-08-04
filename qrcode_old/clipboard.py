#
# clipboard.py
#
# Gestione Clipboard di Windows
#
# Copyright 2026
#

import io

from PIL import Image

import win32clipboard


class ClipboardManager:

    """
    Gestisce la copia delle immagini
    negli appunti di Windows.
    """

    ########################################################

    def __init__(self):

        pass

    ########################################################

    def copy_image(self, image):

        """
        image : PIL.Image
        """

        if image is None:
            return

        output = io.BytesIO()

        #
        # Windows Clipboard accetta
        # immagini DIB (Bitmap)
        #

        image.convert("RGB").save(
            output,
            "BMP"
        )

        data = output.getvalue()[14:]

        output.close()

        win32clipboard.OpenClipboard()

        try:

            win32clipboard.EmptyClipboard()

            win32clipboard.SetClipboardData(

                win32clipboard.CF_DIB,

                data

            )

        finally:

            win32clipboard.CloseClipboard()

    ########################################################

    def clear(self):

        win32clipboard.OpenClipboard()

        try:

            win32clipboard.EmptyClipboard()

        finally:

            win32clipboard.CloseClipboard()

    ########################################################

    def has_image(self):

        win32clipboard.OpenClipboard()

        try:

            return win32clipboard.IsClipboardFormatAvailable(

                win32clipboard.CF_DIB

            )

        finally:

            win32clipboard.CloseClipboard()
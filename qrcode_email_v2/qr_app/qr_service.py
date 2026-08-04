from __future__ import annotations

from pathlib import Path
from urllib.parse import quote, urlencode

import qrcode
from PIL import Image
from qrcode.image.svg import SvgPathImage


class QRService:
    def __init__(self, error_level: str = "H") -> None:
        self.error_level = error_level
        self.foreground = "black"
        self.background = "white"
        self.border = 4
        self.box_size = 10
        self.logo: Image.Image | None = None

    @property
    def correction(self) -> int:
        levels = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }
        return levels.get(self.error_level, levels["H"])

    def set_logo(self, filename: str | Path | None) -> None:
        if self.logo:
            self.logo.close()
        self.logo = Image.open(filename).convert("RGBA") if filename else None

    def create(self, text: str) -> Image.Image:
        if not text.strip():
            raise ValueError("Il contenuto del QR e vuoto")
        qr = qrcode.QRCode(
            error_correction=self.correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(text)
        qr.make(fit=True)
        image = qr.make_image(
            fill_color=self.foreground, back_color=self.background
        ).convert("RGB")
        return self._add_logo(image) if self.logo else image

    def _add_logo(self, image: Image.Image) -> Image.Image:
        logo = self.logo.copy()
        maximum = image.width // 5
        logo.thumbnail((maximum, maximum), Image.Resampling.LANCZOS)
        x = (image.width - logo.width) // 2
        y = (image.height - logo.height) // 2
        image.paste(logo, (x, y), logo)
        return image

    def save_svg(self, text: str, filename: str | Path) -> None:
        qr = qrcode.QRCode(
            error_correction=self.correction,
            box_size=self.box_size,
            border=self.border,
            image_factory=SvgPathImage,
        )
        qr.add_data(text)
        qr.make(fit=True)
        qr.make_image().save(filename)


def build_email_url(recipient: str, description: str, serial: str = "") -> str:
    recipient = recipient.strip()
    description = description.strip()
    serial = serial.strip()
    if "@" not in recipient or any(char in recipient for char in "\r\n,;"):
        raise ValueError("Indirizzo email destinatario non valido")
    if not description:
        raise ValueError("La descrizione e obbligatoria")
    subject = f"Scansione QR - {serial or description[:50]}"
    body = f"DESCRIZIONE: {description}\nSERIALE: {serial}"
    query = urlencode({"subject": subject, "body": body}, quote_via=quote)
    return f"mailto:{quote(recipient, safe='@.+-_')}?{query}"

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Label:
    id: int | None
    description: str
    serial: str
    image_file: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(slots=True)
class Asset:
    id: int | None
    brand: str
    model: str
    serial: str
    user: str = ""
    department: str = ""
    description: str = ""
    created_at: str = ""

    def qr_text(self) -> str:
        rows = [
            ("MARCA", self.brand),
            ("MODELLO", self.model),
            ("SERIALE", self.serial),
            ("UTENTE", self.user),
            ("REPARTO", self.department),
        ]
        return "\n".join(f"{key}: {value}" for key, value in rows if value)

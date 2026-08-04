from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from .paths import data_directory


@dataclass(slots=True)
class AppSettings:
    email_recipient: str = "claudio.pinna@accelleron-industries.com"


class SettingsStore:
    def __init__(self) -> None:
        self.filename = data_directory() / "settings.json"

    def load(self) -> AppSettings:
        if not self.filename.exists():
            return AppSettings()
        try:
            values = json.loads(self.filename.read_text(encoding="utf-8"))
            return AppSettings(
                email_recipient=str(
                    values.get(
                        "email_recipient",
                        "claudio.pinna@accelleron-industries.com",
                    )
                )
            )
        except (OSError, ValueError, TypeError):
            return AppSettings()

    def save(self, settings: AppSettings) -> None:
        self.filename.write_text(
            json.dumps(asdict(settings), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from .models import Asset, Label
from .paths import database_path


class Storage:
    def __init__(self, filename: Path | str | None = None) -> None:
        self.filename = Path(filename) if filename else database_path()
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        self._create_schema()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.filename)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _create_schema(self) -> None:
        with self.connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS labels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    serial TEXT NOT NULL DEFAULT '',
                    image_file TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    model TEXT NOT NULL,
                    serial TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    assigned_user TEXT NOT NULL DEFAULT '',
                    department TEXT NOT NULL DEFAULT '',
                    description TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_labels_serial ON labels(serial);
                CREATE INDEX IF NOT EXISTS idx_assets_serial ON assets(serial);
                """
            )

    def save_label(self, label: Label) -> int:
        with self.connection() as connection:
            if label.id is None:
                cursor = connection.execute(
                    "INSERT INTO labels(description, serial, image_file) VALUES (?, ?, ?)",
                    (label.description, label.serial, label.image_file),
                )
                return int(cursor.lastrowid)
            connection.execute(
                """UPDATE labels
                   SET description=?, serial=?, image_file=?, updated_at=CURRENT_TIMESTAMP
                   WHERE id=?""",
                (label.description, label.serial, label.image_file, label.id),
            )
            return label.id

    def labels(self, search: str = "") -> list[Label]:
        pattern = f"%{search.strip()}%"
        with self.connection() as connection:
            rows = connection.execute(
                """SELECT * FROM labels
                   WHERE description LIKE ? OR serial LIKE ?
                   ORDER BY updated_at DESC, id DESC""",
                (pattern, pattern),
            ).fetchall()
        return [self._label(row) for row in rows]

    def label(self, label_id: int) -> Label | None:
        with self.connection() as connection:
            row = connection.execute(
                "SELECT * FROM labels WHERE id=?", (label_id,)
            ).fetchone()
        return self._label(row) if row else None

    @staticmethod
    def _label(row: sqlite3.Row) -> Label:
        return Label(
            id=row["id"], description=row["description"], serial=row["serial"],
            image_file=row["image_file"], created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def save_asset(self, asset: Asset) -> int:
        with self.connection() as connection:
            if asset.id is None:
                cursor = connection.execute(
                    """INSERT INTO assets
                       (brand, model, serial, assigned_user, department, description)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (asset.brand, asset.model, asset.serial, asset.user,
                     asset.department, asset.description),
                )
                return int(cursor.lastrowid)
            connection.execute(
                """UPDATE assets SET brand=?, model=?, serial=?, assigned_user=?,
                   department=?, description=? WHERE id=?""",
                (asset.brand, asset.model, asset.serial, asset.user,
                 asset.department, asset.description, asset.id),
            )
            return asset.id

    def delete_asset(self, asset_id: int) -> None:
        with self.connection() as connection:
            connection.execute("DELETE FROM assets WHERE id=?", (asset_id,))

    def assets(self, search: str = "") -> list[Asset]:
        pattern = f"%{search.strip()}%"
        with self.connection() as connection:
            rows = connection.execute(
                """SELECT * FROM assets WHERE brand LIKE ? OR model LIKE ?
                   OR serial LIKE ? OR assigned_user LIKE ? OR department LIKE ?
                   ORDER BY id DESC""",
                (pattern, pattern, pattern, pattern, pattern),
            ).fetchall()
        return [
            Asset(
                id=row["id"], brand=row["brand"], model=row["model"],
                serial=row["serial"], user=row["assigned_user"],
                department=row["department"], description=row["description"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def asset(self, asset_id: int) -> Asset | None:
        with self.connection() as connection:
            row = connection.execute("SELECT * FROM assets WHERE id=?", (asset_id,)).fetchone()
        if row is None:
            return None
        return Asset(
            id=row["id"], brand=row["brand"], model=row["model"],
            serial=row["serial"], user=row["assigned_user"],
            department=row["department"], description=row["description"],
            created_at=row["created_at"],
        )

    def add_history(self, title: str, content: str) -> None:
        with self.connection() as connection:
            connection.execute(
                "INSERT INTO history(title, content) VALUES (?, ?)",
                (title, content),
            )

    def history(self, limit: int = 100) -> list[sqlite3.Row]:
        with self.connection() as connection:
            return connection.execute(
                "SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()

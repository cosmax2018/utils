"""Importa i database della versione precedente in QR Generator 2.0."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from qr_app.models import Asset, Label
from qr_app.storage import Storage


def rows(filename: Path, query: str) -> list[sqlite3.Row]:
    if not filename.exists():
        return []
    connection = sqlite3.connect(filename)
    connection.row_factory = sqlite3.Row
    try:
        return connection.execute(query).fetchall()
    finally:
        connection.close()


def migrate(legacy_folder: Path, destination: Storage) -> tuple[int, int, int]:
    data = legacy_folder / "data"
    inventory_file = data / "inventory.db"
    history_file = data / "history.db"
    if not inventory_file.exists():
        inventory_file = legacy_folder / "inventory.db"
    if not history_file.exists():
        history_file = legacy_folder / "history.db"

    label_count = 0
    for row in rows(inventory_file, "SELECT * FROM qr_labels ORDER BY id"):
        destination.save_label(Label(None, row["description"], row["serial"] or "", row["image_file"] or ""))
        label_count += 1

    asset_count = 0
    for row in rows(inventory_file, "SELECT * FROM assets ORDER BY id"):
        asset = Asset(
            None, row["brand"] or "", row["model"] or "", row["serial"] or "",
            row["user"] or "", row["department"] or "", row["description"] or "",
        )
        if not asset.brand or not asset.model or not asset.serial:
            continue
        try:
            destination.save_asset(asset)
            asset_count += 1
        except sqlite3.IntegrityError:
            continue

    history_count = 0
    for row in rows(history_file, "SELECT * FROM history ORDER BY id"):
        destination.add_history(row["title"] or "Importato", row["content"] or "")
        history_count += 1
    return label_count, asset_count, history_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Importa i dati di QR Generator precedente")
    parser.add_argument("cartella", type=Path, help="Cartella qrcode della vecchia versione")
    args = parser.parse_args()
    counts = migrate(args.cartella.resolve(), Storage())
    print(f"Importati: {counts[0]} etichette, {counts[1]} asset, {counts[2]} elementi di cronologia")


if __name__ == "__main__":
    main()

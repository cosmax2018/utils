import unittest
from pathlib import Path

from qr_app.models import Asset, Label
from qr_app.storage import Storage


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.filename = Path(__file__).parent / "_test_storage.db"
        self.filename.unlink(missing_ok=True)
        self.storage = Storage(self.filename)

    def tearDown(self) -> None:
        self.filename.unlink(missing_ok=True)

    def test_label_round_trip_and_search_order(self) -> None:
        label_id = self.storage.save_label(Label(None, "Notebook ufficio", "ABC123"))
        label = self.storage.label(label_id)
        self.assertIsNotNone(label)
        self.assertEqual(label.serial, "ABC123")
        self.assertEqual(label.description, "Notebook ufficio")
        self.assertEqual(self.storage.labels("ABC")[0].id, label_id)

    def test_asset_crud(self) -> None:
        asset = Asset(None, "Dell", "Latitude", "SN001", "Mario", "IT")
        asset.id = self.storage.save_asset(asset)
        loaded = self.storage.asset(asset.id)
        self.assertEqual(loaded.brand, "Dell")
        loaded.user = "Lucia"
        self.storage.save_asset(loaded)
        self.assertEqual(self.storage.asset(asset.id).user, "Lucia")
        self.storage.delete_asset(asset.id)
        self.assertIsNone(self.storage.asset(asset.id))

    def test_history(self) -> None:
        self.storage.add_history("Test", "contenuto")
        row = self.storage.history(1)[0]
        self.assertEqual(row["title"], "Test")


if __name__ == "__main__":
    unittest.main()

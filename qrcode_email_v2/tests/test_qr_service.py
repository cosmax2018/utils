import unittest
from pathlib import Path

from qr_app.qr_service import QRService, build_email_url


class QRServiceTests(unittest.TestCase):
    def test_create_returns_square_rgb_image(self) -> None:
        image = QRService().create("prova QR")
        self.assertEqual(image.mode, "RGB")
        self.assertEqual(image.width, image.height)
        self.assertGreater(image.width, 100)

    def test_empty_text_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            QRService().create("   ")

    def test_svg_is_created(self) -> None:
        filename = Path(__file__).parent / "_test_qr.svg"
        try:
            QRService().save_svg("contenuto", filename)
            self.assertTrue(filename.exists())
            self.assertIn(b"<svg", filename.read_bytes())
        finally:
            filename.unlink(missing_ok=True)

    def test_email_url_encodes_fields(self) -> None:
        url = build_email_url(
            "claudio.pinna@accelleron-industries.com",
            "Pompa olio & filtro",
            "SN 001",
        )
        self.assertTrue(url.startswith("mailto:claudio.pinna@accelleron-industries.com?"))
        self.assertIn("DESCRIZIONE%3A%20Pompa%20olio%20%26%20filtro", url)
        self.assertIn("SERIALE%3A%20SN%20001", url)

    def test_email_requires_valid_recipient(self) -> None:
        with self.assertRaises(ValueError):
            build_email_url("indirizzo-errato", "Prova")


if __name__ == "__main__":
    unittest.main()

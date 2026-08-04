from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont


class LabelService:
    WIDTH = 900
    HEIGHT = 500
    QR_SIZE = 300

    @staticmethod
    def _font(size: int) -> ImageFont.ImageFont:
        for name in ("arial.ttf", "DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return ImageFont.load_default()

    def create(self, qr_image: Image.Image, text: str, font_size: int = 24) -> Image.Image:
        page = Image.new("RGB", (self.WIDTH, self.HEIGHT), "white")
        draw = ImageDraw.Draw(page)
        qr = qr_image.resize((self.QR_SIZE, self.QR_SIZE), Image.Resampling.NEAREST)
        qr_x = 40
        qr_y = (self.HEIGHT - self.QR_SIZE) // 2
        page.paste(qr, (qr_x, qr_y))

        font = self._font(font_size)
        lines = text.splitlines() or [""]
        line_height = font_size + 8
        y = max(20, (self.HEIGHT - len(lines) * line_height) // 2)
        for line in lines:
            draw.text((qr_x + self.QR_SIZE + 40, y), line, fill="black", font=font)
            y += line_height
        return page

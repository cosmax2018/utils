#
# printer.py
#

import os
import tempfile

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class QRPrinter:


    def __init__(self):

        pass


    ##########################################################

    def create_label_image(self, qr_image, title, font_size=24):

        WIDTH = 900
        HEIGHT = 500

        page = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            "white"
        )

        draw = ImageDraw.Draw(page)

        try:
            font = ImageFont.truetype(
                "arial.ttf",
                font_size
            )

        except:

            font = ImageFont.load_default()

        ##########################################################
        # QR a sinistra
        ##########################################################

        QR_SIZE = 300

        qr = qr_image.resize(
            (
                QR_SIZE,
                QR_SIZE
            )
        )

        qr_x = 40
        qr_y = (HEIGHT - QR_SIZE) // 2

        page.paste(
            qr,
            (
                qr_x,
                qr_y
            )
        )

        ##########################################################
        # Testo a destra
        ##########################################################

        text_x = qr_x + QR_SIZE + 40

        lines = title.split("\n")

        line_height = font_size + 8

        total_height = len(lines) * line_height

        y = (HEIGHT - total_height) // 2

        for line in lines:

            draw.text(

                (
                    text_x,
                    y
                ),

                line,

                fill="black",

                font=font

            )

            y += line_height

        return page
        
    def print_label(
            self,
            qr_image,
            title,
            font_size=24
        ):

        page = self.create_label_image(
            qr_image,
            title,
            font_size
        )

        filename = os.path.join(
            tempfile.gettempdir(),
            "qr_label.png"
        )

        page.save(filename)

        os.startfile(filename, "print")
    

        
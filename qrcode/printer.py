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

    def create_label_image(self, qr_image, title):

        WIDTH = 700
        HEIGHT = 950

        page = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            "white"
        )

        draw = ImageDraw.Draw(page)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        #
        # QR
        #

        qr = qr_image.resize((350,350))

        x = (WIDTH-350)//2

        page.paste(qr, (x,40))

        #
        # Testo centrato
        #

        y = 430

        for line in title.split("\n"):

            bbox = draw.textbbox((0,0), line, font=font)

            w = bbox[2]-bbox[0]

            draw.text(
                ((WIDTH-w)//2, y),
                line,
                fill="black",
                font=font
            )

            y += 35

        return page
        
    def print_label(self, qr_image, title):

        page = self.create_label_image(qr_image, title)

        filename = os.path.join(
            tempfile.gettempdir(),
            "qr_label.png"
        )

        page.save(filename)

        os.startfile(filename, "print")
    

        
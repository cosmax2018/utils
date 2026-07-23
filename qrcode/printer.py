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

    def print_label(

        self,

        qr_image,

        title

    ):


        #
        # crea una pagina bianca
        #

        WIDTH = 700
        HEIGHT = 950


        page = Image.new(

            "RGB",

            (WIDTH, HEIGHT),

            "white"

        )


        draw = ImageDraw.Draw(page)


        #
        # font
        #

        try:

            font = ImageFont.truetype(

                "arial.ttf",

                24

            )

        except:

            font = ImageFont.load_default()


        #
        # QR
        #

        qr = qr_image.resize(

            (350,350)

        )


        x = (WIDTH-350)//2

        page.paste(

            qr,

            (x,40)

        )


        #
        # testo centrato
        #

        y = 430

        for line in title.split("\n"):

            # Calcola il rettangolo occupato dal testo
            bbox = draw.textbbox((0, 0), line, font=font)

            text_width = bbox[2] - bbox[0]

            # Coordinata X per centrare il testo
            x = (WIDTH - text_width) // 2

            draw.text(

                (x, y),

                line,

                fill="black",

                font=font

            )

            y += 35


        #
        # salva temporaneamente
        #

        filename = os.path.join(

            tempfile.gettempdir(),

            "qr_label.png"

        )


        page.save(

            filename

        )


        #
        # stampa
        #

        os.startfile(

            filename,

            "print"

        )
        
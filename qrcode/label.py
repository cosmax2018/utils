#
# label.py
#
# Generatore etichette QR Code
#
# Copyright 2026
#

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class LabelGenerator:


    ############################################################

    def __init__(self):

        self.width = 900

        self.height = 520

        self.background = "white"

        self.border = True

        self.title = ""

        self.fields = {}

        self.logo = None


    ############################################################

    def set_size(
            self,
            width,
            height):

        self.width = width

        self.height = height


    ############################################################

    def set_title(
            self,
            title):

        self.title = title


    ############################################################

    def set_fields(
            self,
            fields):

        """
        fields deve essere un dizionario

        esempio:

        {
        "Marca":"HP",
        "Modello":"840 G8",
        "Seriale":"ABC123"
        }

        """

        self.fields = fields


    ############################################################

    def set_logo(
            self,
            filename):

        if filename:

            self.logo = Image.open(
                filename
            )


    ############################################################

    def load_font(
            self,
            size):

        try:

            return ImageFont.truetype(

                "arial.ttf",

                size

            )

        except:

            return ImageFont.load_default()



    ############################################################

    def create(
            self,
            qr_image):


        label = Image.new(

            "RGB",

            (
                self.width,
                self.height
            ),

            self.background

        )


        draw = ImageDraw.Draw(label)


        ##################################################
        # bordo
        ##################################################

        if self.border:

            draw.rectangle(

                (
                    2,
                    2,
                    self.width-2,
                    self.height-2
                ),

                outline="black",

                width=3

            )


        ##################################################
        # QR
        ##################################################

        if qr_image:


            qr = qr_image.resize(

                (
                    330,
                    330
                )

            )


            label.paste(

                qr,

                (
                    40,
                    110
                )

            )


        ##################################################
        # logo
        ##################################################

        if self.logo:


            logo = self.logo.copy()


            logo.thumbnail(

                (
                    100,
                    100
                )

            )


            label.paste(

                logo,

                (
                    self.width-140,
                    30
                ),

                logo if logo.mode=="RGBA"
                else None

            )


        ##################################################
        # testi
        ##################################################

        title_font = self.load_font(36)

        field_font = self.load_font(22)



        draw.text(

            (
                420,
                40
            ),

            self.title,

            fill="black",

            font=title_font

        )


        y = 130


        for key,value in self.fields.items():


            text = f"{key}: {value}"


            draw.text(

                (
                    420,
                    y
                ),

                text,

                fill="black",

                font=field_font

            )


            y += 35



        return label



    ############################################################

    def save(
            self,
            image,
            filename):


        image.save(

            filename

        )



    ############################################################

    def preview(
            self,
            image,
            size=(600,350)):


        return image.resize(

            size,

            Image.Resampling.LANCZOS

        )
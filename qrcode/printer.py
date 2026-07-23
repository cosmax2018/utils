#
# printer.py
#
# Gestione stampa QR Code
#
# Copyright 2026
#

import os
import tempfile

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


class QRPrinter:

    ###########################################################

    def __init__(self):

        self.paper = "A4"

        self.qr_size = 60          # mm

        self.margin = 20           # mm

        self.title = ""

        self.text = ""

    ###########################################################

    def set_title(self,title):

        self.title = title

    ###########################################################

    def set_text(self,text):

        self.text = text

    ###########################################################

    def set_qr_size(self,size_mm):

        self.qr_size = size_mm

    ###########################################################

    def print_image(self,image):

        """
        Stampa tramite il visualizzatore
        predefinito di Windows.
        """

        if image is None:
            return

        filename = os.path.join(
            tempfile.gettempdir(),
            "qr_temp.png"
        )

        image.save(filename)

        os.startfile(filename,"print")

    ###########################################################

    def export_pdf(self,image,filename):

        """
        Crea un PDF A4
        """

        if image is None:
            return

        temp = os.path.join(
            tempfile.gettempdir(),
            "qr_pdf.png"
        )

        image.save(temp)

        c = canvas.Canvas(filename)

        width,height = c._pagesize

        qr = self.qr_size*mm

        x = (width-qr)/2

        y = height-qr-40*mm

        ##################################################

        c.setFont("Helvetica-Bold",18)

        c.drawCentredString(

            width/2,

            height-20*mm,

            self.title

        )

        ##################################################

        c.drawImage(

            temp,

            x,

            y,

            qr,

            qr

        )

        ##################################################

        c.setFont("Helvetica",10)

        yy = y-20

        for line in self.text.splitlines():

            c.drawString(

                25*mm,

                yy,

                line

            )

            yy -= 12

        ##################################################

        c.save()

    ###########################################################

    def export_label(self,image,filename):

        """
        Esporta una etichetta PNG.
        """

        if image is None:
            return

        W = 900

        H = 520

        label = Image.new(

            "RGB",

            (W,H),

            "white"

        )

        draw = ImageDraw.Draw(label)

        ##################################################

        try:

            title_font = ImageFont.truetype(

                "arial.ttf",

                38

            )

            text_font = ImageFont.truetype(

                "arial.ttf",

                22

            )

        except:

            title_font = ImageFont.load_default()

            text_font = ImageFont.load_default()

        ##################################################

        qr = image.resize(

            (320,320)

        )

        label.paste(

            qr,

            (35,90)

        )

        ##################################################

        draw.text(

            (390,60),

            self.title,

            fill="black",

            font=title_font

        )

        ##################################################

        y = 130

        for line in self.text.splitlines():

            draw.text(

                (390,y),

                line,

                fill="black",

                font=text_font

            )

            y += 32

        ##################################################

        label.save(filename)

    ###########################################################

    def preview_label(self,image):

        """
        Restituisce una immagine PIL
        dell'etichetta.
        """

        if image is None:
            return None

        W = 900

        H = 520

        label = Image.new(

            "RGB",

            (W,H),

            "white"

        )

        draw = ImageDraw.Draw(label)

        draw.rectangle(

            (0,0,W-1,H-1),

            outline="black",

            width=2

        )

        qr = image.resize(

            (320,320)

        )

        label.paste(

            qr,

            (35,90)

        )

        try:

            font = ImageFont.truetype(

                "arial.ttf",

                34

            )

        except:

            font = ImageFont.load_default()

        draw.text(

            (390,50),

            self.title,

            font=font,

            fill="black"

        )

        return label
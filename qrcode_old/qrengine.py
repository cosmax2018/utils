#
# qrengine.py
#
# Motore di generazione QR
#

from PIL import Image
from PIL import ImageDraw

import qrcode
import qrcode.image.svg

from pathlib import Path


class QREngine:

    ERROR_LEVELS = {

        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H

    }

    def __init__(self):

        self.box_size = 10

        self.border = 4

        self.foreground = "black"

        self.background = "white"

        self.error_level = "H"

        self.logo = None

        self.image = None

    ######################################################

    def set_box_size(self,size):

        self.box_size = size

    ######################################################

    def set_border(self,border):

        self.border = border

    ######################################################

    def set_foreground(self,color):

        self.foreground = color

    ######################################################

    def set_background(self,color):

        self.background = color

    ######################################################

    def set_error_level(self,level):

        if level in self.ERROR_LEVELS:

            self.error_level = level

    ######################################################

    def set_logo(self,filename):

        if filename is None:

            self.logo = None

            return

        self.logo = Image.open(filename)

    ######################################################

    def create(self,text):

        qr = qrcode.QRCode(

            version=None,

            error_correction=self.ERROR_LEVELS[self.error_level],

            box_size=self.box_size,

            border=self.border

        )

        qr.add_data(text)

        qr.make(fit=True)

        img = qr.make_image(

            fill_color=self.foreground,

            back_color=self.background

        ).convert("RGB")

        if self.logo:

            img = self.add_logo(img)

        self.image = img

        return img

    ######################################################

    def add_logo(self,img):

        logo = self.logo.copy()

        qr_w,qr_h = img.size

        size = qr_w//5

        logo.thumbnail((size,size))

        x = (qr_w-logo.width)//2

        y = (qr_h-logo.height)//2

        img.paste(

            logo,

            (x,y),

            logo if logo.mode=="RGBA" else None

        )

        return img

    ######################################################

    def save_png(self,filename):

        if self.image:

            self.image.save(filename,"PNG")

    ######################################################

    def save_jpg(self,filename):

        if self.image:

            self.image.save(filename,"JPEG",quality=95)

    ######################################################

    def save_bmp(self,filename):

        if self.image:

            self.image.save(filename,"BMP")

    ######################################################

    def save_svg(self,text,filename):

        factory = qrcode.image.svg.SvgImage

        img = qrcode.make(text,image_factory=factory)

        img.save(filename)

    ######################################################

    def resize(self,size):

        if self.image is None:

            return None

        return self.image.resize(

            (size,size),

            Image.Resampling.LANCZOS

        )

    ######################################################

    def get_image(self):

        return self.image

    ######################################################

    def get_size(self):

        if self.image is None:

            return 0,0

        return self.image.size

    ######################################################

    def clear(self):

        self.image = None
#
# settings.py
#
# Gestione configurazioni QRGenerator Professional
#
# Copyright 2026
#

import configparser
from pathlib import Path


class Settings:

    ############################################################

    def __init__(self, filename="config.ini"):

        self.filename = Path(filename)

        self.config = configparser.ConfigParser()

        self.load()

    ############################################################

    def load(self):

        """
        Carica configurazione esistente.
        Se non esiste crea quella predefinita.
        """

        if self.filename.exists():

            self.config.read(
                self.filename,
                encoding="utf8"
            )

        else:

            self.create_default()

            self.save()

    ############################################################

    def create_default(self):

        self.config["GENERAL"] = {

            "theme": "System",

            "language": "IT",

            "last_folder": "",

            "last_printer": ""

        }


        self.config["WINDOW"] = {

            "width": "1100",

            "height": "760",

            "x": "100",

            "y": "100"

        }


        self.config["QR"] = {

            "foreground": "black",

            "background": "white",

            "error_level": "H",

            "box_size": "10",

            "border": "4",

            "default_size": "420"

        }


        self.config["FILES"] = {

            "last_png": "",

            "last_pdf": "",

            "last_logo": ""

        }


        self.config["LABEL"] = {

            "title_font": "Arial",

            "title_size": "34",

            "paper": "A4",

            "label_width": "900",

            "label_height": "520"

        }

    ############################################################

    def save(self):

        """
        Salva configurazione su disco.
        """

        with open(

            self.filename,

            "w",

            encoding="utf8"

        ) as f:

            self.config.write(f)

    ############################################################

    def get(self,section,key,fallback=None):

        try:

            return self.config[section][key]

        except KeyError:

            return fallback

    ############################################################

    def set(self,section,key,value):

        if section not in self.config:

            self.config[section] = {}

        self.config[section][key] = str(value)

        self.save()

    ############################################################

    #
    # Funzioni rapide per QR
    #

    ############################################################

    def get_qr_settings(self):

        return {

            "foreground":

                self.get(
                    "QR",
                    "foreground",
                    "black"
                ),

            "background":

                self.get(
                    "QR",
                    "background",
                    "white"
                ),

            "error_level":

                self.get(
                    "QR",
                    "error_level",
                    "H"
                ),

            "box_size":

                int(
                    self.get(
                        "QR",
                        "box_size",
                        10
                    )
                ),

            "border":

                int(
                    self.get(
                        "QR",
                        "border",
                        4
                    )
                )

        }

    ############################################################

    def set_qr_settings(
            self,
            foreground,
            background,
            error_level,
            box_size,
            border):


        self.set(
            "QR",
            "foreground",
            foreground
        )

        self.set(
            "QR",
            "background",
            background
        )

        self.set(
            "QR",
            "error_level",
            error_level
        )

        self.set(
            "QR",
            "box_size",
            box_size
        )

        self.set(
            "QR",
            "border",
            border
        )

    ############################################################

    #
    # Finestra
    #

    ############################################################

    def save_window_geometry(
            self,
            geometry):

        self.set(
            "WINDOW",
            "geometry",
            geometry
        )

    ############################################################

    def get_window_geometry(self):

        return self.get(

            "WINDOW",

            "geometry",

            "1100x760"

        )

    ############################################################

    #
    # Cartelle
    #

    ############################################################

    def set_last_folder(self,path):

        self.set(

            "GENERAL",

            "last_folder",

            str(path)

        )

    ############################################################

    def get_last_folder(self):

        return self.get(

            "GENERAL",

            "last_folder",

            ""

        )

    ############################################################

    #
    # Logo
    #

    ############################################################

    def set_logo(self,path):

        self.set(

            "FILES",

            "last_logo",

            str(path)

        )

    ############################################################

    def get_logo(self):

        return self.get(

            "FILES",

            "last_logo",

            ""

        )
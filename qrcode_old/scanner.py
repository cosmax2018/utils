#
# scanner.py
#
# Lettura QR Code / Barcode
#
# Supporta:
# - scanner USB HID
# - webcam
#
# Copyright 2026
#

import json


class QRScanner:


    ############################################################

    def __init__(self, database=None):

        self.database = database

        self.last_code = None


    ############################################################

    def set_database(self, database):

        self.database = database



    ############################################################

    def decode_text(self, text):

        """
        Riceve il testo letto dal QR.

        Se il QR contiene JSON
        restituisce un dizionario.

        Altrimenti restituisce testo.
        """


        self.last_code = text


        try:

            return json.loads(text)


        except Exception:

            return text



    ############################################################

    def find_asset(self, text):

        """
        Cerca un asset nel database.

        Funziona con:
        - JSON QR
        - seriale semplice
        """


        if self.database is None:

            return None



        data = self.decode_text(text)



        ##################################################
        # QR JSON
        ##################################################

        if isinstance(data,dict):


            serial = data.get(

                "SERIALE",

                ""

            )


            if serial:

                return self.database.find_serial(

                    serial

                )



        ##################################################
        # QR testo normale
        ##################################################

        return self.database.find_serial(

            text

        )



    ############################################################

    def parse_asset_json(self,text):

        """
        Converte QR inventario JSON
        in dizionario.
        """

        try:

            return json.loads(text)


        except:

            return {}



###############################################################
#
# Scanner HID USB
#
###############################################################


class HIDScanner:


    def __init__(self):

        self.buffer = ""



    def add_character(self,char):

        """
        Riceve caratteri come
        una tastiera.

        """

        if char == "\n":

            result = self.buffer

            self.buffer = ""

            return result


        self.buffer += char


        return None
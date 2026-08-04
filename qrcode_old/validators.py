#
# validators.py
#
# Validazione dati inventario
#
# Copyright 2026
#



class Validator:



    ############################################################

    def __init__(self):

        self.errors = []



    ############################################################

    def clear(self):

        self.errors.clear()



    ############################################################

    def valid(self):

        return len(

            self.errors

        ) == 0



    ############################################################

    def add_error(
            self,
            message):

        self.errors.append(

            message

        )



    ############################################################

    def validate_asset(
            self,
            asset):


        self.clear()



        required = [

            "brand",

            "model",

            "serial"

        ]



        for field in required:


            value = asset.get(

                field,

                ""

            )


            if not value.strip():


                self.add_error(

                    f"Campo obbligatorio mancante: {field}"

                )



        serial = asset.get(

            "serial",

            ""

        )



        if len(serial) < 3:


            self.add_error(

                "Seriale troppo corto"

            )



        return self.valid()



    ############################################################

    def validate_length(
            self,
            text,
            max_length,
            name):


        if len(text) > max_length:


            self.add_error(

                f"{name} supera {max_length} caratteri"

            )

            return False



        return True



    ############################################################

    def validate_serial_unique(
            self,
            serial,
            database):


        result = database.find_serial(

            serial

        )


        if result:


            self.add_error(

                f"Seriale già presente: {serial}"

            )


            return False



        return True



    ############################################################

    def get_errors(self):

        return self.errors



    ############################################################

    def validate_qr_text(
            self,
            text):


        if not text:


            self.add_error(

                "Il contenuto QR è vuoto"

            )


            return False



        if len(text) > 4000:


            self.add_error(

                "Contenuto QR troppo lungo"

            )


            return False



        return True
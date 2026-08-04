#
# batch.py
#
# Generazione massiva QR / Etichette
#
# Copyright 2026
#

from pathlib import Path

from qrengine import QREngine

from label import LabelGenerator

from utils import (

    create_asset_qr_data,

    safe_filename,

    timestamp

)



class BatchGenerator:


    ############################################################

    def __init__(

            self,

            database=None,

            history=None):


        self.database = database

        self.history = history


        self.output_folder = Path(

            "output"

        )


        self.output_folder.mkdir(

            exist_ok=True

        )


        self.generated = 0

        self.errors = 0



    ############################################################

    def set_output_folder(

            self,

            folder):


        self.output_folder = Path(folder)


        self.output_folder.mkdir(

            parents=True,

            exist_ok=True

        )



    ############################################################

    def generate(

            self,

            assets,

            callback=None):


        """

        assets:

        lista di dizionari inventario


        callback:

        funzione richiamata ad ogni elemento

        """



        self.generated = 0

        self.errors = 0



        total = len(assets)



        for index,asset in enumerate(assets):


            try:


                self.generate_one(

                    asset

                )


                self.generated += 1



            except Exception:


                self.errors += 1



            if callback:


                callback(

                    index+1,

                    total

                )



        return (

            self.generated,

            self.errors

        )



    ############################################################

    def generate_one(

            self,

            asset):



        brand = asset.get(

            "brand",

            asset.get(

                "Marca",

                ""

            )

        )



        model = asset.get(

            "model",

            asset.get(

                "Modello",

                ""

            )

        )



        serial = asset.get(

            "serial",

            asset.get(

                "Seriale",

                ""

            )

        )



        user = asset.get(

            "user",

            asset.get(

                "Utente",

                ""

            )

        )



        department = asset.get(

            "department",

            asset.get(

                "Reparto",

                ""

            )

        )



        ##################################################
        # testo QR
        ##################################################


        qr_text = create_asset_qr_data(

            brand,

            model,

            serial,

            user,

            department

        )



        ##################################################
        # nome file
        ##################################################


        filename = safe_filename(

            serial

        )



        if filename=="":

            filename="asset"



        png_file = (

            self.output_folder /

            (

                filename +

                "_qr.png"

            )

        )



        label_file = (

            self.output_folder /

            (

                filename +

                "_label.png"

            )

        )



        ##################################################
        # QR
        ##################################################


        qr = QREngine()


        qr.create(

            qr_text

        )


        qr.save_png(

            png_file

        )



        ##################################################
        # Etichetta
        ##################################################


        label = LabelGenerator()


        label.set_title(

            f"{brand} {model}"

        )


        label.set_fields({

            "Seriale":

                serial,


            "Utente":

                user,


            "Reparto":

                department

        })


        label_img = label.create(

            qr.get_image()

        )


        label.save(

            label_img,

            label_file

        )



        ##################################################
        # database
        ##################################################


        if self.database:


            self.database.add_asset(

                category="Asset",

                brand=brand,

                model=model,

                serial=serial,

                user=user,

                department=department,

                qr_text=qr_text

            )



        ##################################################
        # history
        ##################################################


        if self.history:


            self.history.add(

                title=f"{brand} {model}",

                content=qr_text,

                png=str(png_file)

            )
#
# import_export.py
#
# Import / Export inventario
#
# Copyright 2026
#

import csv

from pathlib import Path

import json


try:

    from openpyxl import load_workbook

    EXCEL_AVAILABLE = True


except ImportError:

    EXCEL_AVAILABLE = False



from utils import create_asset_qr_data



class InventoryIO:


    ############################################################

    def __init__(self):

        pass



    ############################################################

    def import_csv(
            self,
            filename):


        assets=[]


        with open(

            filename,

            "r",

            encoding="utf8"

        ) as file:


            reader = csv.DictReader(file)


            for row in reader:


                assets.append(row)



        return assets



    ############################################################

    def export_csv(

            self,

            filename,

            assets):


        if not assets:

            return



        fields = list(

            assets[0].keys()

        )


        with open(

            filename,

            "w",

            newline="",

            encoding="utf8"

        ) as file:


            writer = csv.DictWriter(

                file,

                fieldnames=fields

            )


            writer.writeheader()


            writer.writerows(

                assets

            )



    ############################################################

    def import_excel(

            self,

            filename):


        if not EXCEL_AVAILABLE:


            raise RuntimeError(

                "Modulo openpyxl non installato"

            )



        workbook = load_workbook(

            filename,

            data_only=True

        )


        sheet = workbook.active


        rows = list(

            sheet.values

        )


        if len(rows)<2:

            return []



        headers = rows[0]


        assets=[]



        for row in rows[1:]:


            item={}



            for key,value in zip(

                headers,

                row

            ):


                if key:

                    item[str(key)] = (

                        ""

                        if value is None

                        else str(value)

                    )


            assets.append(item)



        return assets



    ############################################################

    def export_json(

            self,

            filename,

            assets):


        with open(

            filename,

            "w",

            encoding="utf8"

        ) as file:


            json.dump(

                assets,

                file,

                indent=4,

                ensure_ascii=False

            )



    ############################################################

    def create_qr_text(

            self,

            asset):


        """

        Riceve un dizionario inventario

        e crea il contenuto QR.

        """

        return create_asset_qr_data(

            asset.get(

                "Marca",

                asset.get(

                    "brand",

                    ""

                )

            ),


            asset.get(

                "Modello",

                asset.get(

                    "model",

                    ""

                )

            ),


            asset.get(

                "Seriale",

                asset.get(

                    "serial",

                    ""

                )

            ),


            asset.get(

                "Utente",

                asset.get(

                    "user",

                    ""

                )

            ),


            asset.get(

                "Reparto",

                asset.get(

                    "department",

                    ""

                )

            )

        )



    ############################################################

    def normalize_asset(

            self,

            asset):


        """

        Uniforma i nomi dei campi.

        """

        result={}



        mapping={


            "Marca":

                "brand",


            "Modello":

                "model",


            "Seriale":

                "serial",


            "Utente":

                "user",


            "Reparto":

                "department",


            "Sede":

                "location"


        }



        for key,value in asset.items():


            new_key = mapping.get(

                key,

                key

            )


            result[new_key]=value



        return result



    ############################################################

    def create_batch_folder(

            self,

            folder):


        path = Path(folder)


        path.mkdir(

            parents=True,

            exist_ok=True

        )


        return path
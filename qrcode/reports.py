#
# reports.py
#
# Generazione report inventario
#
# Copyright 2026
#

from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import A4

from reportlab.lib.units import mm

from datetime import datetime



class InventoryReport:


    ############################################################

    def __init__(self):

        self.title = "Inventario Asset"



    ############################################################

    def set_title(
            self,
            title):

        self.title = title



    ############################################################

    def create_pdf(
            self,
            assets,
            filename):


        c = canvas.Canvas(

            filename,

            pagesize=A4

        )


        width,height = A4



        y = height - 25*mm



        ##################################################
        # titolo
        ##################################################


        c.setFont(

            "Helvetica-Bold",

            18

        )


        c.drawString(

            20*mm,

            y,

            self.title

        )


        y -= 15*mm



        c.setFont(

            "Helvetica",

            9

        )


        c.drawString(

            20*mm,

            y,

            "Generato: " +

            datetime.now()
            .strftime(
                "%d/%m/%Y %H:%M"
            )

        )


        y -= 15*mm



        ##################################################
        # intestazione
        ##################################################


        c.setFont(

            "Helvetica-Bold",

            9

        )


        c.drawString(

            20*mm,

            y,

            "Marca"

        )


        c.drawString(

            55*mm,

            y,

            "Modello"

        )


        c.drawString(

            100*mm,

            y,

            "Seriale"

        )


        c.drawString(

            140*mm,

            y,

            "Utente"

        )


        y -= 8*mm



        c.setFont(

            "Helvetica",

            8

        )



        ##################################################
        # dati
        ##################################################


        for asset in assets:


            if y < 20*mm:

                c.showPage()

                y = height-20*mm



            #

            # asset arriva dal database
            # come tupla

            #

            try:

                brand = asset[3]

                model = asset[4]

                serial = asset[5]

                user = asset[7]


            except:

                continue



            c.drawString(

                20*mm,

                y,

                str(brand)

            )


            c.drawString(

                55*mm,

                y,

                str(model)[:25]

            )


            c.drawString(

                100*mm,

                y,

                str(serial)

            )


            c.drawString(

                140*mm,

                y,

                str(user)[:20]

            )


            y -= 6*mm



        c.save()



    ############################################################

    def create_user_report(
            self,
            assets,
            user,
            filename):


        filtered=[]



        for asset in assets:


            if asset[7] == user:

                filtered.append(asset)



        self.create_pdf(

            filtered,

            filename

        )



    ############################################################

    def create_department_report(
            self,
            assets,
            department,
            filename):


        filtered=[]



        for asset in assets:


            if asset[8] == department:

                filtered.append(asset)



        self.create_pdf(

            filtered,

            filename

        )



    ############################################################

    def statistics(
            self,
            assets):


        result={

            "totale": len(assets),

            "marche": {},

            "modelli": {}

        }



        for asset in assets:


            brand = asset[3]

            model = asset[4]



            result["marche"][brand] = (

                result["marche"].get(

                    brand,

                    0

                ) + 1

            )



            result["modelli"][model] = (

                result["modelli"].get(

                    model,

                    0

                ) + 1

            )



        return result
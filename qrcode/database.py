#
# database.py
#
# Database inventario QRGenerator Professional
#
# Copyright 2026
#

import sqlite3

from datetime import datetime



class InventoryDatabase:


    ############################################################

    def __init__(
            self,
            filename="inventory.db"):


        self.filename = filename


        self.conn = sqlite3.connect(
            self.filename
        )


        self.cursor = self.conn.cursor()


        self.create_tables()



    ############################################################

    def create_tables(self):


        self.cursor.execute(
        """

        CREATE TABLE IF NOT EXISTS assets
        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,


            created TEXT,


            category TEXT,


            brand TEXT,


            model TEXT,


            serial TEXT UNIQUE,


            asset_code TEXT,


            user TEXT,


            department TEXT,


            location TEXT,


            notes TEXT,


            qr_text TEXT


        )

        """
        )


        self.conn.commit()



    ############################################################

    def add_asset(
            self,
            category,
            brand,
            model,
            serial,
            asset_code="",
            user="",
            department="",
            location="",
            notes="",
            qr_text=""):



        self.cursor.execute(
        """

        INSERT INTO assets

        (

        created,
        category,
        brand,
        model,
        serial,
        asset_code,
        user,
        department,
        location,
        notes,
        qr_text

        )


        VALUES (?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

        datetime.now()
        .strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        category,

        brand,

        model,

        serial,

        asset_code,

        user,

        department,

        location,

        notes,

        qr_text

        )


        )


        self.conn.commit()



    ############################################################

    def update_asset(
            self,
            asset_id,
            **fields):


        allowed = [

            "category",

            "brand",

            "model",

            "serial",

            "asset_code",

            "user",

            "department",

            "location",

            "notes",

            "qr_text"

        ]


        values=[]


        query=[]



        for key,value in fields.items():


            if key in allowed:

                query.append(
                    f"{key}=?"
                )

                values.append(value)



        if not query:

            return



        values.append(asset_id)



        sql = """

        UPDATE assets

        SET

        """

        sql += ",".join(query)

        sql += """

        WHERE id=?

        """



        self.cursor.execute(
            sql,
            values
        )


        self.conn.commit()



    ############################################################

    def delete_asset(
            self,
            asset_id):


        self.cursor.execute(

            """
            DELETE FROM assets

            WHERE id=?

            """,

            (
                asset_id,
            )

        )


        self.conn.commit()



    ############################################################

    def get_asset(
            self,
            asset_id):


        self.cursor.execute(

            """

            SELECT *

            FROM assets

            WHERE id=?

            """,

            (
                asset_id,
            )

        )


        return self.cursor.fetchone()



    ############################################################

    def get_all(self):


        self.cursor.execute(

            """

            SELECT *

            FROM assets

            ORDER BY id DESC

            """

        )


        return self.cursor.fetchall()



    ############################################################

    def search(
            self,
            text):


        value = "%" + text + "%"



        self.cursor.execute(

        """

        SELECT *

        FROM assets


        WHERE

        brand LIKE ?

        OR

        model LIKE ?

        OR

        serial LIKE ?

        OR

        user LIKE ?

        OR

        asset_code LIKE ?


        ORDER BY id DESC


        """,

        (

        value,

        value,

        value,

        value,

        value

        )

        )


        return self.cursor.fetchall()



    ############################################################

    def find_serial(
            self,
            serial):


        self.cursor.execute(

            """

            SELECT *

            FROM assets

            WHERE serial=?

            """,

            (
                serial,
            )

        )


        return self.cursor.fetchone()



    ############################################################

    def count(self):


        self.cursor.execute(

            """

            SELECT COUNT(*)

            FROM assets

            """

        )


        return self.cursor.fetchone()[0]



    ############################################################

    def export_csv(
            self,
            filename):


        import csv



        rows = self.get_all()



        with open(

            filename,

            "w",

            newline="",

            encoding="utf8"

        ) as f:



            writer = csv.writer(f)



            writer.writerow(

            [

            "ID",

            "DATA",

            "TIPO",

            "MARCA",

            "MODELLO",

            "SERIALE",

            "CODICE",

            "UTENTE",

            "REPARTO",

            "SEDE",

            "NOTE",

            "QR"

            ]

            )



            writer.writerows(rows)



    ############################################################

    def close(self):


        self.conn.close()
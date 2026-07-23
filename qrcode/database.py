#
# database.py
#
# Gestione database inventario SQLite
#
# Copyright 2026
#

import sqlite3

from pathlib import Path
import sys



############################################################
#
# percorso applicazione
#
############################################################


def application_path():

    """
    Restituisce la cartella dell'applicazione.

    Funziona sia:
    - da Python
    - da PyInstaller .exe
    """

    if getattr(sys, "frozen", False):

        # eseguibile PyInstaller

        return Path(
            sys.executable
        ).parent


    else:

        # esecuzione normale Python

        return Path(
            __file__
        ).parent



############################################################
#
# database path
#
############################################################


DATA_FOLDER = application_path() / "data"


DATA_FOLDER.mkdir(

    exist_ok=True

)



DB_FILE = DATA_FOLDER / "inventory.db"





class InventoryDatabase:


    ########################################################

    def __init__(self):


        self.db_file = DB_FILE


        self.create_database()



    ########################################################

    def connect(self):


        return sqlite3.connect(

            self.db_file

        )



    ########################################################

    def create_database(self):


        conn = self.connect()


        cur = conn.cursor()

        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS qr_labels(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            description TEXT NOT NULL,

            serial TEXT,

            image_file TEXT,

            created TEXT,

            updated TEXT
        )
        """
        )        

        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS assets
        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,


            category TEXT,


            brand TEXT,


            model TEXT,


            serial TEXT UNIQUE,


            description TEXT,


            purchase_date TEXT,


            user TEXT,


            department TEXT,


            qr_text TEXT,


            created TEXT

        )

        """
        )


        conn.commit()

        conn.close()



    ########################################################

    def add_label(

           self,

           description,

           serial,

           image_file

       ):

       from datetime import datetime

       conn = self.connect()

       cur = conn.cursor()

       now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

       cur.execute(

           """
           INSERT INTO qr_labels(

               description,

               serial,

               image_file,

               created,

               updated

           )

           VALUES(?,?,?,?,?)

           """,

           (

               description,

               serial,

               image_file,

               now,

               now

           )

       )

       conn.commit()

       label_id = cur.lastrowid

       conn.close()

       return label_id
    
    def add_asset(

            self,

            category,

            brand,

            model,

            serial,

            user="",

            department="",

            qr_text="",

            description="",

            purchase_date=""

    ):


        conn = self.connect()

        cur = conn.cursor()



        cur.execute(

        """

        INSERT INTO assets

        (

        category,

        brand,

        model,

        serial,

        description,

        purchase_date,

        user,

        department,

        qr_text,

        created

        )

        VALUES (?,?,?,?,?,?,?,?,?,datetime('now'))

        """,

        (

        category,

        brand,

        model,

        serial,

        description,

        purchase_date,

        user,

        department,

        qr_text

        )


        )


        conn.commit()

        conn.close()



    ########################################################
    
    def update_label(

            self,

            label_id,

            description,

            serial,

            image_file

        ):

        from datetime import datetime

        conn = self.connect()

        cur = conn.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute(

            """

            UPDATE qr_labels

            SET

                description=?,

                serial=?,

                image_file=?,

                updated=?

            WHERE id=?

            """,

            (

                description,

                serial,

                image_file,

                now,

                label_id

            )

        )

        conn.commit()

        conn.close()
        

    def get_all(self):


        conn = self.connect()

        cur = conn.cursor()


        cur.execute(

            "SELECT * FROM assets ORDER BY id DESC"

        )


        rows = cur.fetchall()


        conn.close()


        return rows



    ########################################################

    def get_labels(self):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(

            """

            SELECT

                id,
                
                description,
                
                serial,

                image_file,
                
                created,

                updated

            FROM qr_labels

            ORDER BY updated DESC

            """

        )

        rows = cur.fetchall()

        conn.close()

        return rows
    
    def get_label(

            self,

            label_id

        ):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(

            """

            SELECT *

            FROM qr_labels

            WHERE id=?

            """,

            (

                label_id,

            )

        )

        row = cur.fetchone()

        conn.close()

        return row
    
    def get_asset(self, asset_id):


        conn = self.connect()

        cur = conn.cursor()


        cur.execute(

            "SELECT * FROM assets WHERE id=?",

            (asset_id,)

        )


        row = cur.fetchone()


        conn.close()


        return row



    ########################################################

    def search_labels(

            self,

            text

        ):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute(

            """

            SELECT

                id,

                serial,

                description,

                updated

            FROM qr_labels

            WHERE

                serial LIKE ?

                OR

                description LIKE ?

            ORDER BY updated DESC

            """,

            (

                "%" + text + "%",

                "%" + text + "%"

            )

        )

        rows = cur.fetchall()

        conn.close()

        return rows
    
    def find_serial(self, serial):


        conn = self.connect()

        cur = conn.cursor()


        cur.execute(

            "SELECT * FROM assets WHERE serial=?",

            (serial,)

        )


        row = cur.fetchone()


        conn.close()


        return row



    ########################################################

    def search(self, text):


        conn = self.connect()

        cur = conn.cursor()



        pattern = f"%{text}%"



        cur.execute(

        """

        SELECT * FROM assets

        WHERE brand LIKE ?

        OR model LIKE ?

        OR serial LIKE ?

        OR user LIKE ?

        """,

        (

        pattern,

        pattern,

        pattern,

        pattern

        )


        )


        rows = cur.fetchall()


        conn.close()


        return rows
        
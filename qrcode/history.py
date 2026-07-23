#
# history.py
#
# Cronologia QR generati
#
# Copyright 2026
#


import sqlite3

from pathlib import Path

import sys



############################################################

def application_path():


    if getattr(sys, "frozen", False):

        return Path(

            sys.executable

        ).parent


    return Path(

        __file__

    ).parent





DATA_FOLDER = application_path() / "data"


DATA_FOLDER.mkdir(

    exist_ok=True

)



DB_FILE = DATA_FOLDER / "history.db"





class History:



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

        CREATE TABLE IF NOT EXISTS history

        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,


            date TEXT,


            title TEXT,


            content TEXT,


            png TEXT


        )

        """

        )



        conn.commit()

        conn.close()



    ########################################################

    def add(

            self,

            title,

            content,

            png=""

    ):


        conn = self.connect()

        cur = conn.cursor()



        cur.execute(

        """

        INSERT INTO history

        (

            date,

            title,

            content,

            png

        )

        VALUES

        (

            datetime('now'),

            ?,

            ?,

            ?

        )

        """,

        (

            title,

            content,

            png

        )

        )


        conn.commit()

        conn.close()



    ########################################################

    def get_last(

            self,

            limit=100

    ):


        conn = self.connect()

        cur = conn.cursor()



        cur.execute(

        """

        SELECT *

        FROM history

        ORDER BY id DESC

        LIMIT ?

        """,

        (

            limit,

        )

        )


        rows = cur.fetchall()


        conn.close()


        return rows

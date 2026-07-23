#
# history.py
#
# Gestione cronologia QR Code
#
# Copyright 2026
#

import sqlite3
from datetime import datetime
import hashlib


class History:

    ############################################################

    def __init__(self, dbname="history.db"):

        self.dbname = dbname

        self.conn = sqlite3.connect(self.dbname)

        self.cursor = self.conn.cursor()

        self.create_table()

    ############################################################

    def create_table(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            created TEXT,

            title TEXT,

            content TEXT,

            sha256 TEXT,

            png TEXT,

            pdf TEXT,

            foreground TEXT,

            background TEXT,

            error_level TEXT,

            qr_size INTEGER,

            logo TEXT

        )

        """)

        self.conn.commit()

    ############################################################

    def add(self,
            title,
            content,
            png="",
            pdf="",
            foreground="black",
            background="white",
            error_level="H",
            qr_size=10,
            logo=""):

        digest = hashlib.sha256(
            content.encode("utf8")
        ).hexdigest()

        self.cursor.execute("""

        INSERT INTO history(

            created,

            title,

            content,

            sha256,

            png,

            pdf,

            foreground,

            background,

            error_level,

            qr_size,

            logo

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            title,

            content,

            digest,

            png,

            pdf,

            foreground,

            background,

            error_level,

            qr_size,

            logo

        ))

        self.conn.commit()

    ############################################################

    def delete(self,id):

        self.cursor.execute(

            "DELETE FROM history WHERE id=?",

            (id,)

        )

        self.conn.commit()

    ############################################################

    def clear(self):

        self.cursor.execute(

            "DELETE FROM history"

        )

        self.conn.commit()

    ############################################################

    def count(self):

        self.cursor.execute(

            "SELECT COUNT(*) FROM history"

        )

        return self.cursor.fetchone()[0]

    ############################################################

    def get(self,id):

        self.cursor.execute(

            "SELECT * FROM history WHERE id=?",

            (id,)

        )

        return self.cursor.fetchone()

    ############################################################

    def get_last(self,n=20):

        self.cursor.execute("""

        SELECT *

        FROM history

        ORDER BY id DESC

        LIMIT ?

        """,

        (n,)

        )

        return self.cursor.fetchall()

    ############################################################

    def search(self,text):

        self.cursor.execute("""

        SELECT *

        FROM history

        WHERE

        title LIKE ?

        OR

        content LIKE ?

        ORDER BY id DESC

        """,

        (

            "%"+text+"%",

            "%"+text+"%"

        )

        )

        return self.cursor.fetchall()

    ############################################################

    def exists(self,content):

        digest = hashlib.sha256(

            content.encode("utf8")

        ).hexdigest()

        self.cursor.execute("""

        SELECT id

        FROM history

        WHERE sha256=?

        """,

        (digest,)

        )

        return self.cursor.fetchone() is not None

    ############################################################

    def export_csv(self,filename):

        import csv

        self.cursor.execute(

            "SELECT * FROM history"

        )

        rows = self.cursor.fetchall()

        with open(

            filename,

            "w",

            newline="",

            encoding="utf8"

        ) as f:

            writer = csv.writer(f)

            writer.writerow([

                "ID",

                "DATA",

                "TITOLO",

                "CONTENUTO",

                "SHA256",

                "PNG",

                "PDF",

                "FG",

                "BG",

                "ERR",

                "SIZE",

                "LOGO"

            ])

            writer.writerows(rows)

    ############################################################

    def close(self):

        self.conn.close()
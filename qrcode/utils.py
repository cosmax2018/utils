#
# utils.py
#
# Funzioni di utilità QRGenerator Professional
#
# Copyright 2026
#

from pathlib import Path

from datetime import datetime

import hashlib

import json

import shutil

import re



#############################################################
#
# Cartelle
#
#############################################################


def create_folder(path):

    """
    Crea una cartella se non esiste.
    """

    folder = Path(path)

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



#############################################################
#
# Data e ora
#
#############################################################


def timestamp():

    return datetime.now().strftime(

        "%Y%m%d_%H%M%S"

    )



def timestamp_readable():

    return datetime.now().strftime(

        "%d/%m/%Y %H:%M:%S"

    )



#############################################################
#
# Nomi file
#
#############################################################


def safe_filename(text):

    """
    Trasforma un testo in un nome file valido Windows.
    """

    text = re.sub(

        r'[<>:"/\\|?*]',

        "_",

        text

    )


    text = text.replace(

        " ",

        "_"

    )


    return text



def create_filename(
        title,
        extension="png"):


    name = safe_filename(title)


    return (

        name +

        "_" +

        timestamp()

        +

        "."

        +

        extension

    )



#############################################################
#
# Hash
#
#############################################################


def sha256(text):

    return hashlib.sha256(

        text.encode(
            "utf8"
        )

    ).hexdigest()



#############################################################
#
# QR inventario
#
#############################################################


def asset_to_text(asset):

    """
    Converte un dizionario inventario
    in testo leggibile per QR.
    """


    lines=[]


    for key,value in asset.items():


        if value:

            lines.append(

                f"{key}: {value}"

            )


    return "\n".join(lines)



def asset_to_json(asset):

    """
    Crea JSON per QR strutturati.
    """

    return json.dumps(

        asset,

        indent=4,

        ensure_ascii=False

    )



def json_to_asset(text):

    return json.loads(text)



#############################################################
#
# Backup
#
#############################################################


def backup_file(
        source,
        destination):


    shutil.copy2(

        source,

        destination

    )



#############################################################
#
# Conversioni
#
#############################################################


def bytes_to_mb(value):

    return round(

        value / (1024*1024),

        2

    )



def mm_to_pixel(
        mm,
        dpi=300):

    """

    Conversione mm -> pixel

    utile per stampa etichette.

    """

    return int(

        mm *

        dpi /

        25.4

    )



#############################################################
#
# Validazioni
#
#############################################################


def is_empty(value):

    if value is None:

        return True


    if str(value).strip()=="":

        return True


    return False



def validate_serial(serial):

    """
    Controllo seriale generico.
    """

    if is_empty(serial):

        return False


    return len(serial.strip()) >= 3



#############################################################
#
# QR inventario predefinito
#
#############################################################


def create_asset_qr_data(

        brand,

        model,

        serial,

        user="",

        department=""):


    data={


        "TIPO":

            "ASSET",


        "MARCA":

            brand,


        "MODELLO":

            model,


        "SERIALE":

            serial,


        "UTENTE":

            user,


        "REPARTO":

            department

    }


    return asset_to_json(data)
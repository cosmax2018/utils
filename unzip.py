# --------------------------------------------------------
# unzip.py : script python per scompattare un file zippato
# --------------------------------------------------------

import zipfile, os, argparse

# Creiamo il parser dei parametri da linea di comando
parser = argparse.ArgumentParser(description="Decomprime un file ZIP in una cartella specificata.")
parser.add_argument("zipfile", help="Percorso del file ZIP da decomprimere")
parser.add_argument("dest", help="Cartella di destinazione per i file decompressi")

# Leggiamo i parametri
args = parser.parse_args()
zip_path = args.zipfile
extract_to = args.dest

# Creiamo la cartella di destinazione se non esiste
os.makedirs(extract_to, exist_ok=True)

# Apriamo e decomprimiamo il file ZIP
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print(f"File decompressi in '{extract_to}'")


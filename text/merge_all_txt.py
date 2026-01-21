
#
# merge_all_txt.py :    prende tutti i file .txt presenti in una directory
#                       li unisce (merge) in un unico file di testo
#                       precede ciascun contenuto con un titolo chiaramente visibile
#                       il titolo è il nome del file senza estensione
#                       mantiene l’ordine alfabetico dei file (utile e prevedibile)

import os
from pathlib import Path

def read_text_safely(path):
    """Legge un file di testo gestendo encoding non UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")
        
def merge_txt_files(input_dir, output_file):
    input_dir = Path(input_dir)
    txt_files = sorted(input_dir.glob("*.txt"))

    if not txt_files:
        print("Nessun file .txt trovato.")
        return

    with open(output_file, "w", encoding="utf-8") as outfile:
        for txt_file in txt_files:
            title = txt_file.stem

            outfile.write("\n")
            outfile.write("=" * 80 + "\n")
            outfile.write(title + "\n")
            outfile.write("=" * 80 + "\n\n")

            content = read_text_safely(txt_file)
            outfile.write(content.rstrip() + "\n")

    print(f"Merge completato → {output_file}")

# -------------------------------
# ESEMPIO DI UTILIZZO
# -------------------------------
if __name__ == "__main__":
    directory_input = r"D:\miei-scritti"
    file_output = r"D:\miei-scritti\__MERGE_di_tutti_i_TXT.txt"

    merge_txt_files(directory_input, file_output)

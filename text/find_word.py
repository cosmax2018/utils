
#
# find_word.py : Cerca in tutti i file di testo, ignorando i file binari
#                Mostra nome file + numero riga + contenuto riga
#                Non si blocca su errori di encoding

import os

def cerca_parola(cartella, parola_chiave):
    for root, dirs, files in os.walk(cartella):
        for nome_file in files:
            percorso_file = os.path.join(root, nome_file)

            try:
                with open(percorso_file, "r", encoding="utf-8", errors="ignore") as f:
                    for numero_riga, riga in enumerate(f, start=1):
                        if parola_chiave.lower() in riga.lower():
                            print(f"Trovato in: {percorso_file}")
                            print(f"  Riga {numero_riga}: {riga.strip()}")
                            print("-" * 60)

            except Exception as e:
                # Se il file non è leggibile (binario, permessi, ecc.)
                pass


if __name__ == "__main__":
    cartella_da_cercare = r"D:\miei-github-repositories"
    parola = "cluster"

    cerca_parola(cartella_da_cercare, parola)
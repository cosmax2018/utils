# confronto_registro_chiavi.py
import os

file_prima = "prima.reg"
file_dopo = "dopo.reg"

def leggi_file(filename):
    with open(filename, "r", encoding="utf-16") as f:
        return [line.rstrip() for line in f]

righe_prima = leggi_file(file_prima)
righe_dopo = leggi_file(file_dopo)

chiave_corrente_prima = None
chiave_corrente_dopo = None

print("\n=== DIFFERENZE TROVATE ===\n")

for i in range(max(len(righe_prima), len(righe_dopo))):
    riga_p = righe_prima[i] if i < len(righe_prima) else ""
    riga_d = righe_dopo[i] if i < len(righe_dopo) else ""

    # Aggiorna chiave corrente
    if riga_p.startswith("[HKEY_"):
        chiave_corrente_prima = riga_p
    if riga_d.startswith("[HKEY_"):
        chiave_corrente_dopo = riga_d

    # Se la riga è diversa e non è vuota
    if riga_p != riga_d:
        chiave_mostrata = chiave_corrente_dopo or chiave_corrente_prima or "<Chiave sconosciuta>"
        print(f"🗝️  Chiave: {chiave_mostrata}")

        if riga_p and riga_d:
            print(f"  Prima: {riga_p}")
            print(f"  Dopo : {riga_d}")
        elif riga_p and not riga_d:
            print(f"  Rimossa: {riga_p}")
        elif riga_d and not riga_p:
            print(f"  Aggiunta: {riga_d}")

        print("-" * 70)

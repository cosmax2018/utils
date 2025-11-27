# confronta_registri_binario.py
file_prima = "prima.reg"
file_dopo = "dopo.reg"

# Funzione per leggere file .reg con encoding corretto
def leggi_file(filename):
    with open(filename, "r", encoding="utf-16") as f:
        return [line.strip() for line in f]

righe_prima = leggi_file(file_prima)
righe_dopo = leggi_file(file_dopo)

# Trova differenze riga per riga
max_len = max(len(righe_prima), len(righe_dopo))
for i in range(max_len):
    riga_p = righe_prima[i] if i < len(righe_prima) else "<NESSUNA RIGA>"
    riga_d = righe_dopo[i] if i < len(righe_dopo) else "<NESSUNA RIGA>"
    if riga_p != riga_d:
        print(f"Riga {i+1} differente:")
        print(f"  Prima: {riga_p}")
        print(f"  Dopo : {riga_d}")
        print("-"*50)

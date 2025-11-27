# estrai_diff_reg.py
import re

file_prima = "prima.reg"
file_dopo = "dopo.reg"
file_output = "differenze.reg"

def leggi_file(filename):
    with open(filename, "r", encoding="utf-16") as f:
        return [line.strip() for line in f]

def estrai_blocchi(lines):
    """
    Divide il file .reg in blocchi:
    ogni chiave [HKEY_...] e i suoi valori associati
    """
    blocchi = {}
    current_key = None
    current_values = []

    for line in lines:
        if line.startswith("[HKEY_"):
            if current_key:
                blocchi[current_key] = current_values
            current_key = line.strip()
            current_values = []
        elif current_key:
            current_values.append(line.strip())
    if current_key:
        blocchi[current_key] = current_values

    return blocchi

righe_prima = leggi_file(file_prima)
righe_dopo = leggi_file(file_dopo)

blocchi_prima = estrai_blocchi(righe_prima)
blocchi_dopo = estrai_blocchi(righe_dopo)

differenze = {}

for key, values_dopo in blocchi_dopo.items():
    values_prima = blocchi_prima.get(key, [])
    if values_prima != values_dopo:
        differenze[key] = {
            "prima": values_prima,
            "dopo": values_dopo
        }

# Scrivi solo i blocchi che differiscono in un nuovo file .reg
with open(file_output, "w", encoding="utf-16") as out:
    out.write("Windows Registry Editor Version 5.00\n\n")
    for key, diff in differenze.items():
        out.write(f"{key}\n")
        for line in diff["dopo"]:
            if line:  # evita righe vuote
                out.write(f"{line}\n")
        out.write("\n")

print(f"[✓] File '{file_output}' creato con le differenze trovate.")
print("Controlla questo file per vedere quale chiave e valore è cambiato (es. Duplex, TwoSided, ecc.).")

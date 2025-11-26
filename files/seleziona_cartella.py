
#
# seleziona_cartella.py : apre una finestra e consente di selezionare una cartella.
#

import tkinter as tk
from tkinter import filedialog

def seleziona_cartella():
    cartella_selezionata = filedialog.askdirectory()
    finestra.destroy()  # Chiude la finestra dopo la selezione della cartella
    return cartella_selezionata  # Restituisce il percorso della cartella selezionata

def seleziona():
    global finestra
    finestra = tk.Tk()
    finestra.title("Seleziona una cartella")

    larghezza_finestra = 400
    altezza_finestra = 200
    finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}")

    # Aspetta che la finestra di dialogo sia chiusa prima di proseguire
    cartella_selezionata = seleziona_cartella()

    if cartella_selezionata:
        print("Cartella selezionata:", cartella_selezionata)
        return cartella_selezionata
    else:
        print("Nessuna cartella selezionata")
        return None

if __name__ == "__main__":
    seleziona()
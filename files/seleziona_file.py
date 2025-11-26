
#
# seleziona_file.py : apre una finestra e consente di selezionare un file.
#
# In questo script, abbiamo 4 funzioni (seleziona_file_m4a, seleziona_file_wav, seleziona_file_mp3, seleziona_file_3ga),
# ciascuna progettata per aprire una finestra di dialogo per selezionare file con una specifica estensione (.m4a, .wav, .mp3, .3ga).
# Utilizziamo l'argomento filetypes del metodo askopenfilename per filtrare i file visualizzati nella finestra di dialogo in base all'estensione.
# Dopo la selezione del file, il percorso del file selezionato viene stampato e la finestra principale viene chiusa.

import tkinter as tk
from tkinter import filedialog

tipo = None

def seleziona_file_m4a():
    global tipo
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.m4a")])
    if file_path:
        # print("File selezionato:", file_path)
        finestra.file_selezionato = file_path
        tipo = 'm4a'
        finestra.destroy()

def seleziona_file_wav():
    global tipo
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
    if file_path:
        # print("File selezionato:", file_path)
        finestra.file_selezionato = file_path
        tipo = 'wav'
        finestra.destroy()

def seleziona_file_mp3():
    global tipo
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3")])
    if file_path:
        # print("File selezionato:", file_path)
        finestra.file_selezionato = file_path
        tipo = 'mp3'
        finestra.destroy()

def seleziona_file_3ga():
    global tipo
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.3ga")])
    if file_path:
        # print("File selezionato:", file_path)
        finestra.file_selezionato = file_path
        tipo = '3ga'
        finestra.destroy()
        
def seleziona():
    global finestra
    finestra = tk.Tk()
    finestra.title("Seleziona un file audio")

    larghezza_finestra = 400
    altezza_finestra = 200
    finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}")

    tk.Button(finestra, text="Seleziona .m4a", command=seleziona_file_m4a).pack(pady=10)
    tk.Button(finestra, text="Seleziona .wav", command=seleziona_file_wav).pack(pady=10)
    tk.Button(finestra, text="Seleziona .mp3", command=seleziona_file_mp3).pack(pady=10)
    tk.Button(finestra, text="Seleziona .3ga", command=seleziona_file_3ga).pack(pady=10)

    finestra.mainloop()
    
    if hasattr(finestra, 'file_selezionato'):
        # print("File selezionato:", finestra.file_selezionato)
        return finestra.file_selezionato, tipo
    else:
        # print("Nessun file selezionato")
        return None, None    

if __name__ == "__main__":
    seleziona()

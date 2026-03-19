# seleziona_file_4.py : apre una finestra e consente di selezionare un file di un certo tipo.

import sys
import tkinter as tk
from tkinter import filedialog

def seleziona_file(type):
    global tipo
    file_path = filedialog.askopenfilename(filetypes=[("Files type", f"*.{type}")])
    if file_path:
        print("File selezionato:", file_path)
        finestra.file_selezionato = file_path
        tipo = type
        finestra.destroy()
        
def seleziona(argv):
    
    global finestra
    finestra = tk.Tk()
    finestra.title("Seleziona il file")
    
    larghezza_finestra = 400
    altezza_finestra = 200

    finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}")
    
    testo_etichetta = f"Seleziona un file {argv[0]}"
    etichetta = tk.Label(finestra, text=testo_etichetta, font=("Helvetica", 16))
    etichetta.pack(pady=20)

    # Pulsante per aprire la finestra di selezione file
    pulsante = tk.Button(finestra, text="Sfoglia", command=seleziona_file, width=20, height=2)
    pulsante.pack(pady=20)

    # Posiziona il pulsante al centro della finestra
    finestra.update_idletasks()
    larghezza_pulsante = pulsante.winfo_width()
    finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}+{int((finestra.winfo_screenwidth() - larghezza_finestra) / 2)}+{int((finestra.winfo_screenheight() - altezza_finestra) / 2)}")

    finestra.mainloop()

    if hasattr(finestra, 'file_selezionato'):
        # print("File selezionato:", finestra.file_selezionato)
        return finestra.file_selezionato, tipo
    else:
        # print("Nessun file selezionato")
        return None, None

if __name__ == "__main__":
    seleziona(sys.argv[1:])        
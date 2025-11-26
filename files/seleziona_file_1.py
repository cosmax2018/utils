
# seleziona_file.py : apre una finestra e consente di selezionare un file.

import tkinter as tk
from tkinter import filedialog

def seleziona_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        finestra.destroy()  # Chiude la finestra dopo la selezione del file
        finestra.file_selezionato = file_path

def seleziona():
    global finestra
    finestra = tk.Tk()
    finestra.title("Seleziona il file")
    
    larghezza_finestra = 400
    altezza_finestra = 200

    finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}")
    
    testo_etichetta = "Seleziona un file di testo .txt"
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
        return finestra.file_selezionato
    else:
        # print("Nessun file selezionato")
        return None

if __name__ == "__main__":
    seleziona()







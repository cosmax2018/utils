import tkinter as tk
from tkinter import filedialog

def seleziona_file():
    global tipo
    file_path = filedialog.askopenfilename(
        filetypes=[("Files type", f"*.{tipo}")]
    )
    if file_path:
        finestra.file_selezionato = file_path
        finestra.destroy()

def seleziona(tipo_file):
    global finestra, tipo
    tipo = tipo_file

    finestra = tk.Tk()
    finestra.title("Seleziona il file")

    larghezza_finestra = 400
    altezza_finestra = 200
    finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}")

    etichetta = tk.Label(
        finestra,
        text=f"Seleziona un file .{tipo}",
        font=("Helvetica", 16)
    )
    etichetta.pack(pady=20)

    pulsante = tk.Button(
        finestra,
        text="Sfoglia",
        command=seleziona_file,
        width=20,
        height=2
    )
    pulsante.pack(pady=20)

    finestra.mainloop()

    if hasattr(finestra, 'file_selezionato'):
        return finestra.file_selezionato, tipo
    else:
        return None, None

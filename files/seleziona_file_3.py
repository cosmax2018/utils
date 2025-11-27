
# seleziona_file.py : apre una finestra e consente di selezionare un file video .mp4

import tkinter as tk
from tkinter import filedialog

tipo = None

def seleziona_file_m4a():
    global tipo
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if file_path:
        print("File selezionato:", file_path)
        finestra.file_selezionato = file_path
        tipo = 'mp4'
        finestra.destroy()
        
def seleziona():
    global finestra
    finestra = tk.Tk()
    finestra.title("Seleziona un file video")

    larghezza_finestra = 400
    altezza_finestra = 200
    finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}")

    tk.Button(finestra, text="Seleziona .mp4", command=seleziona_file_m4a).pack(pady=10)

    finestra.mainloop()
    
    if hasattr(finestra, 'file_selezionato'):
        # print("File selezionato:", finestra.file_selezionato)
        return finestra.file_selezionato, tipo
    else:
        # print("Nessun file selezionato")
        return None, None    

if __name__ == "__main__":
    seleziona()

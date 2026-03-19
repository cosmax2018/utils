
#
# find_word-gui.py : Cerca in tutti i file di testo, ignorando i file binari
#                    Mostra nome file + numero riga + contenuto riga
#                    Non si blocca su errori di encoding
#                    Versione GUI di find_word.py

import os
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


class CercaParolaGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Ricerca Parola nei File")
        self.root.geometry("900x600")

        # Frame superiore
        frame_top = tk.Frame(root)
        frame_top.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_top, text="Cartella:").grid(row=0, column=0, sticky="w")

        self.entry_cartella = tk.Entry(frame_top)
        self.entry_cartella.grid(row=0, column=1, sticky="ew", padx=5)

        btn_sfoglia = tk.Button(frame_top, text="Sfoglia", command=self.scegli_cartella)
        btn_sfoglia.grid(row=0, column=2, padx=5)

        tk.Label(frame_top, text="Parola chiave:").grid(row=1, column=0, sticky="w", pady=5)

        self.entry_parola = tk.Entry(frame_top)
        self.entry_parola.grid(row=1, column=1, sticky="ew", padx=5)

        btn_cerca = tk.Button(frame_top, text="Cerca", command=self.avvia_ricerca)
        btn_cerca.grid(row=1, column=2, padx=5)

        frame_top.columnconfigure(1, weight=1)

        # Area risultati
        self.area_risultati = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.area_risultati.pack(fill="both", expand=True, padx=10, pady=10)

        # Pulsante salva
        btn_salva = tk.Button(root, text="Salva Risultati", command=self.salva_risultati)
        btn_salva.pack(pady=5)

    def scegli_cartella(self):
        cartella = filedialog.askdirectory()
        if cartella:
            self.entry_cartella.delete(0, tk.END)
            self.entry_cartella.insert(0, cartella)

    def avvia_ricerca(self):
        cartella = self.entry_cartella.get()
        parola = self.entry_parola.get()

        if not cartella or not parola:
            messagebox.showwarning("Attenzione", "Inserisci cartella e parola chiave.")
            return

        self.area_risultati.delete("1.0", tk.END)

        thread = threading.Thread(target=self.cerca_parola, args=(cartella, parola))
        thread.start()

    def cerca_parola(self, cartella, parola_chiave):
        trovati = 0

        for file in Path(cartella).rglob("*"):
            if file.is_file():
                try:
                    with open(file, "r", encoding="utf-8", errors="ignore") as f:
                        for numero_riga, riga in enumerate(f, start=1):
                            if parola_chiave.lower() in riga.lower():
                                trovati += 1
                                risultato = (
                                    f"File: {file}\n"
                                    f"Riga {numero_riga}: {riga.strip()}\n"
                                    f"{'-'*70}\n"
                                )
                                self.area_risultati.insert(tk.END, risultato)
                                self.area_risultati.see(tk.END)
                except:
                    pass

        self.area_risultati.insert(tk.END, f"\nRicerca completata. Occorrenze trovate: {trovati}\n")

    def salva_risultati(self):
        contenuto = self.area_risultati.get("1.0", tk.END)
        if not contenuto.strip():
            messagebox.showinfo("Info", "Nessun risultato da salvare.")
            return

        file_salvataggio = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("File di testo", "*.txt")]
        )

        if file_salvataggio:
            with open(file_salvataggio, "w", encoding="utf-8") as f:
                f.write(contenuto)
            messagebox.showinfo("Salvato", "Risultati salvati correttamente.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CercaParolaGUI(root)
    root.mainloop()
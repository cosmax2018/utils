# -------------------------------------------------------------------------------------------
#
# interface.py : interfaccia grafica a finestre per la conversione fra i formati di documenti
#                PDF e Word.
#
# -------------------------------------------------------------------------------------------
#
# written by Massimiliano Cosmelli ( @_°° massimiliano.cosmelli@accelleron-industries.com )
#
#                   CopyRight 2025-2026 Accelleron Industries 
#
# -------------------------------------------------------------------------------------------
#
# interfaccia a finestre molto semplice che mi permette di scegliere il file da convertire da una finestra di dialogo. 
# E con due pulsanti, uno per convertire da pdf a word e uno per convertire da word a pdf. Premendo il primo esegue lo
# script pdf2word_v2.py passandogli il nome del file .pdf da convertire. Premendo il secondo pulsante esegue lo script
# word2pdf.py passandogli il nome del file .doc/.docx da convertire. Entrambi gli script si trovano nella sottocartella
# /conversion e i risultati della conversione vengono messi nella stessa cartella locale da cui sono stati presi i files
# da convertire.
#
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from pdf2word import converti as pdf_to_word
from word2pdf import converti as word_to_pdf
import sys
from tkinter import ttk
import threading

# Funzione per selezionare il file
def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        p = Path(file_path)  # normalizzazione        
        entry_file.delete(0, tk.END)
        entry_file.insert(0, str(p))

# fondamentale: NON bloccare la GUI
def run_with_progress(func, file_path):
    def task():
        try:
            func(file_path)
            log("✔ Conversione completata")
        except Exception as e:
            log(f"❌ Errore: {e}")
        finally:
            progress.stop()

    progress.start(10)  # velocità animazione
    threading.Thread(target=task, daemon=True).start()
    
# Funzione per convertire PDF -> Word
def convert_pdf_to_word():
    file_path = Path(entry_file.get())
    
    if file_path.suffix.lower() not in (".pdf"):
        messagebox.showerror("Errore", "Seleziona un file PDF!")
        return

    try:
        # pdf_to_word(file_path)
        run_with_progress(pdf_to_word, file_path)
        messagebox.showinfo("Fatto", f"Conversione completata!\nSalvato in {file_path}")
    except Exception as e:
        messagebox.showerror("Errore", f"Conversione fallita:\n{e}")


# Funzione per convertire Word -> PDF
def convert_word_to_pdf():
    file_path = Path(entry_file.get())
    
    if file_path.suffix.lower() not in (".doc", ".docx"):
        messagebox.showerror("Errore", "Seleziona un file Word (.doc/.docx)!")
        return
    
    try:
        # word_to_pdf(file_path)
        run_with_progress(word_to_pdf, file_path)
        messagebox.showinfo("Fatto", f"Conversione completata!\nSalvato in {file_path}")
    except Exception as e:
        messagebox.showerror("Errore", f"Conversione fallita:\n{e}")


# --- Interfaccia Tkinter ---
root = tk.Tk()
root.title("PDF ↔ Word Converter")
root.geometry("500x150")
root.resizable(False, False)

frame_file = tk.Frame(root)
frame_file.pack(pady=10, padx=10, fill=tk.X)

entry_file = tk.Entry(frame_file, width=40)
entry_file.pack(side=tk.LEFT, padx=(0,5), expand=True, fill=tk.X)

btn_browse = tk.Button(frame_file, text="Sfoglia", command=select_file)
btn_browse.pack(side=tk.LEFT)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_pdf2word = tk.Button(frame_buttons, text="PDF → Word", width=20, command=convert_pdf_to_word)
btn_pdf2word.pack(side=tk.LEFT, padx=5)

btn_word2pdf = tk.Button(frame_buttons, text="Word → PDF", width=20, command=convert_word_to_pdf)
btn_word2pdf.pack(side=tk.LEFT, padx=5)

progress = ttk.Progressbar(root, mode="indeterminate")
progress.pack(fill=tk.X, padx=15, pady=(10,30))

root.mainloop()
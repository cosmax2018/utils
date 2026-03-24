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
# /conversion e i risultati della conversione devono essere messi nella cartella locale /Download
#
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# Percorsi cartelle
conversion_dir = os.path.join(os.getcwd(), "conversion")
download_dir = os.path.join(os.getcwd(), "Download")
os.makedirs(download_dir, exist_ok=True)

# Funzione per selezionare il file
def select_file():
    file_path = filedialog.askopenfilename()
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

# Funzione per convertire PDF -> Word
def convert_pdf_to_word():
    file_path = entry_file.get()
    if not file_path.lower().endswith(".pdf"):
        messagebox.showerror("Errore", "Seleziona un file PDF!")
        return
    
    script_path = os.path.join(os.getcwd(), "pdf2word.py")
    
    # Nome file di output
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(download_dir, base_name + ".docx")
    
    try:
        subprocess.run(["python", script_path, file_path, output_file], check=True)
        messagebox.showinfo("Fatto", f"Conversione completata!\nSalvato in {output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Errore", f"Conversione fallita:\n{e}")

# Funzione per convertire Word -> PDF
def convert_word_to_pdf():
    file_path = entry_file.get()
    if not file_path.lower().endswith((".doc", ".docx")):
        messagebox.showerror("Errore", "Seleziona un file Word (.doc/.docx)!")
        return
    
    script_path = os.path.join(os.getcwd(),"word2pdf.py")
    
    # Nome file di output
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(download_dir, base_name + ".pdf")
    
    try:
        subprocess.run(["python", script_path, file_path, output_file], check=True)
        messagebox.showinfo("Fatto", f"Conversione completata!\nSalvato in {output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Errore", f"Conversione fallita:\n{e}")

# --- Interfaccia Tkinter ---
root = tk.Tk()
root.title("PDF ↔ Word Converter")
root.geometry("500x110")
root.resizable(False, False)

# Frame per selezione file
frame_file = tk.Frame(root)
frame_file.pack(pady=10, padx=10, fill=tk.X)

entry_file = tk.Entry(frame_file, width=40)
entry_file.pack(side=tk.LEFT, padx=(0,5), expand=True, fill=tk.X)

btn_browse = tk.Button(frame_file, text="Sfoglia", command=select_file)
btn_browse.pack(side=tk.LEFT)

# Frame per pulsanti conversione
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_pdf2word = tk.Button(frame_buttons, text="PDF → Word", width=20, command=convert_pdf_to_word)
btn_pdf2word.pack(side=tk.LEFT, padx=5)

btn_word2pdf = tk.Button(frame_buttons, text="Word → PDF", width=20, command=convert_word_to_pdf)
btn_word2pdf.pack(side=tk.LEFT, padx=5)

root.mainloop()
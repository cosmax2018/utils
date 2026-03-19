
# pdf2doc.py : conversione .pdf -> .docx

import pdfplumber
from docx import Document

# Percorso del file PDF di input
pdf_path = input("File .pdf: ") # es. "input.pdf"
# Percorso del file Word di output
docx_path = "output.docx"   # l'output viene rinominato cosi'

# Crea un nuovo documento Word
doc = Document()

# Apri il PDF
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        # Estrai il testo dalla pagina
        text = page.extract_text()
        if text:
            # Aggiungi il testo al documento Word
            doc.add_paragraph(text)
            # Aggiungi una pagina nuova (opzionale)
            doc.add_page_break()

# Salva il documento Word
doc.save(docx_path)

print(f"Conversione completata! File salvato come {docx_path}")
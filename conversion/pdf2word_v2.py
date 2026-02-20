
# pdf2doc_v2.py :   conversione .pdf -> .docx
#                   conserva laa formattazione e le tabelle

from pdf2docx import Converter

# Percorso del PDF di input
pdf_file = input("Nome file .pdf : ")  # "input.pdf"
# Percorso del file Word di output
docx_file = "output.docx"

# Crea il convertitore
cv = Converter(pdf_file)

# Converti tutto il PDF in Word
cv.convert(docx_file, start=0, end=None)  # start e end sono gli indici delle pagine

# Chiudi il convertitore
cv.close()

print(f"Conversione completata! File salvato come {docx_file}")
#
# word2pdf.py : conversione .docxpdf -> .pdf
#
from pathlib import Path
import sys
import win32com.client

def converti(file_path):
    file_path = Path(file_path)

    print(f"Conversione di {file_path}")

    output_file = file_path.with_suffix(".pdf")

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    try:
        doc = word.Documents.Open(str(file_path))
        doc.SaveAs(str(output_file), FileFormat=17)  # 17 = PDF
        doc.Close()
    finally:
        word.Quit()

    print(f"Conversione completata! File salvato come {output_file}")

if __name__ == "__main__":
    converti(sys.argv[1])
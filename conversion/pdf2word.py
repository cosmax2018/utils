#
# pdf2word.py :   conversione .pdf -> .docx
#                 conserva la formattazione e le tabelle
import os,sys
from pathlib import Path
from pdf2docx import Converter

def converti(file_path):  
    # converte da .pdf a .docx
    #
    # utilizzo:  > from pdf2word import converti
    #            > converti("C:\Users\ITMACOS\pippo.pdf")
    #
    # oppure:    > py pdf2word.py C:\Users\ITMACOS\pippo.pdf
    #
    file_path = Path(file_path)  # ← IMPORTANTISSIMO
    
    print(f"Conversione di {file_path}")
    
    file_name = file_path.name                                      # pippo.pdf
    file_name_without_ext = file_path.stem                          # pippo    
    folder_path = file_path.parent                                  # "C:\Users\ITMACOS\"
    output_file = folder_path / (file_name_without_ext + ".docx")   # pippo.docx
    
    # Crea il convertitore
    # cv = Converter(file_name)
    cv = Converter(str(file_path))

    # Converti tutto il PDF in Word
    # cv.convert(output_file, start=0, end=None)  # start e end sono gli indici delle pagine
    cv.convert(str(output_file), start=0, end=None)

    # Chiudi il convertitore
    cv.close()

    print(f"Conversione completata! File salvato come {output_file}")

if __name__ == "__main__":
    converti(sys.argv[1])
    
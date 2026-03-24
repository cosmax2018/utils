#
# pdf2word.py :   conversione .pdf -> .docx
#                 conserva la formattazione e le tabelle
import os,sys
from pdf2docx import Converter

def converti(file_path):  
    # converte da .pdf a .docx
    #
    # utilizzo:  > from pdf2word import converti
    #            > converti("C:\Users\ITMACOS\pippo.pdf")
    #
    # oppure:    > py pdf2word.py C:\Users\ITMACOS\pippo.pdf
    #
    file_path = file_path[0]
    print(f"Conversione di {file_path}")
    file_name = os.path.basename(file_path)                                  # pippo.pdf
    file_name_without_ext = os.path.splitext(file_name)[0]                   # pippo
    
    folder_path = os.path.dirname(file_path)                                 # "C:\Users\ITMACOS\"
    output_file = os.path.join(folder_path, file_name_without_ext + ".docx") # pippo.docx
    
    # Crea il convertitore
    cv = Converter(file_name)

    # Converti tutto il PDF in Word
    cv.convert(output_file, start=0, end=None)  # start e end sono gli indici delle pagine

    # Chiudi il convertitore
    cv.close()

    print(f"Conversione completata! File salvato come {output_file}")

if __name__ == "__main__":
    converti(sys.argv[1:])
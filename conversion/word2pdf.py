#
# word2pdf.py : converte un file word .docx in .pdf
#
import os,sys
from docx2pdf import convert
from seleziona_file_4 import seleziona

# Converte un singolo file da word a pdf

def rename_to_pdf(file_name):
    # rinomina il file in un .pdf
    base, _ = os.path.splitext(file_name)
    return base + ".pdf"

    # os.rename(file, nuovo_file)

def main():
    #
    # e.g.:  py word2pdf.py    (apre una finestra di dialogo)
	#
    
    nome_del_file_da_convertire, tipo = seleziona('docx')
    nome_del_file_convertito = rename_to_pdf(nome_del_file_da_convertire)
    
    print("DEBUG file:", nome_del_file_da_convertire)
    print("DEBUG tipo:", tipo)
    print("DEBUG pdf:", nome_del_file_convertito)
    
    convert(nome_del_file_da_convertire, 
            nome_del_file_convertito)
    
    print(f"convertito {nome_del_file_da_convertire} in {nome_del_file_convertito}")

if __name__ == "__main__":
    main()
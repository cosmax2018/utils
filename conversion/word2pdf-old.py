#
# word2pdf.py : conversione .docxpdf -> .pdf
#
import os,sys
from pathlib import Path
from docx2pdf import convert

def converti(file_path):  
    # converte da .docx a .pdf
    #
    # utilizzo:  > from word2pdf import converti
    #            > converti("C:\Users\ITMACOS\pippo.docx")
    #
    # oppure:    > py word2pdf.py C:\Users\ITMACOS\pippo.docx
    #
    file_path = Path(file_path)  # ← fondamentale
    
    print(f"Conversione di {file_path}")
    
    # file_name = file_path.name                                      # pippo.docx
    # file_name_without_ext = file_path.stem                          # pippo
    # folder_path = file_path.parent                                  # "C:\Users\ITMACOS\"
    # output_file = folder_path / (file_name_without_ext + ".pdf")    # pippo.pdf
    
    output_file = file_path.with_suffix(".pdf")
    
    # print(f"\n{file_name}\n{file_name_without_ext}\n{output_file}\n")

    # convert(file_name,output_file)
    # convert(str(file_path), str(output_file))
    convert(str(file_path))
    
    print(f"Conversione completata! File salvato come {output_file}")

if __name__ == "__main__":
    converti(sys.argv[1])
#
# word2pdf.py : conversione .docxpdf -> .pdf
#
import os,sys
from docx2pdf import convert

def converti(file_path):  
    # converte da .docx a .pdf
    #
    # utilizzo:  > from word2pdf import converti
    #            > converti("C:\Users\ITMACOS\pippo.docx")
    #
    # oppure:    > py word2pdf.py C:\Users\ITMACOS\pippo.docx
    #
    file_path = file_path[0]
    print(f"Conversione di {file_path}")
    file_name = os.path.basename(file_path)                                  # pippo.docx
    file_name_without_ext = os.path.splitext(file_name)[0]                   # pippo
    
    folder_path = os.path.dirname(file_path)                                 # "C:\Users\ITMACOS\"
    output_file = os.path.join(folder_path, file_name_without_ext + ".pdf") # pippo.pdf
    
    print(f"\n{file_name}\n{file_name_without_ext}\n{output_file}\n")

    convert(file_name,output_file)

    print(f"Conversione completata! File salvato come {output_file}")

if __name__ == "__main__":
    converti(sys.argv[1:])    
#
# word2pdf.py : converte un file word .docx in .pdf
#
import sys
from docx2pdf import convert

# Converte un singolo file da word a pdf

def main(argv):
    
    # e.g.:  word2pdf pippo.docx pippo.pdf
	
	convert(argv[0], argv[1])
    
    print(f"convertito {argv[0]} in {argv[1]}")

if __name__ == "__main__":
    main(sys.argv[1:])
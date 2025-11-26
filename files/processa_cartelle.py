
#
# processa_cartelle.py : data una lista di cartelle processa i files audio contenuti in esse.
#

from elenca_files import elenca_files
from processa_files_audio import processa_files

# cartelle = ['W:\mie-registrazioni-audio\cartella 001', \
			# 'W:\mie-registrazioni-audio\cartella 002', \
			# 'W:\mie-registrazioni-audio\cartella 003', \
			# 'W:\mie-registrazioni-audio\cartella 004', \
			# 'W:\mie-registrazioni-audio\cartella 005', \
			# 'W:\mie-registrazioni-audio\cartella 006', \
			# 'W:\mie-registrazioni-audio\cartella 007', \  <<----
			# 'W:\mie-registrazioni-audio\cartella 008', \
			# 'W:\mie-registrazioni-audio\cartella 009', \
			# 'W:\mie-registrazioni-audio\cartella 010', \
			# 'W:\mie-registrazioni-audio\cartella 011', \
			# 'W:\mie-registrazioni-audio\cartella 012']
			
cartelle = ['W:\mie-registrazioni-audio\cartella 007']
			
if __name__ == "__main__":
	
    for cartella in cartelle:
        percorso_cartella,lista_files_tipi = elenca_files(cartella)
        processa_files(percorso_cartella,lista_files_tipi)

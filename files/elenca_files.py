
#
# elenca_files.py : data una cartella elenca i files presenti ed il relativo tipo restituendo
#					una lista di tuple:[(nome_del_file1, estens_del_file1), (nome_del_file2, estens_del_file2), ...]

import os

from seleziona_cartella import seleziona

FILE,TIPO = 0,1

def elenca_files_e_estensioni(cartella):
    # Creare una lista vuota per memorizzare le coppie [nome_file, estensione_file]
    lista_files_estensioni = []

    # Elencare tutti i file nella cartella specificata
    for nome_file in os.listdir(cartella):
        # Ottenere il percorso completo del file
        percorso_completo = os.path.join(cartella, nome_file)

        # Controllare se è un file (e non una cartella)
        if os.path.isfile(percorso_completo):
            # Ottenere l'estensione del file
            _, estensione = os.path.splitext(nome_file)

            # Se l'estensione non viene identificata, impostarla come 'Sconosciuta'
            if estensione == '':
                estensione = 'Sconosciuta'

            # Aggiungere la coppia [nome_file, estensione] alla lista
            lista_files_estensioni.append((nome_file, estensione[1:]))

    return lista_files_estensioni

def elenca_files(percorso_cartella,stampa=False):
    # Elenca i files all'interno della cartella indicata

    lista_files_tipi = elenca_files_e_estensioni(percorso_cartella)
    
    if stampa == True:
        print(f'\nFiles presenti nella cartella {percorso_cartella} : \n')
        for file_e_tipo in lista_files_tipi:
                print(f'File: {file_e_tipo[FILE]} - Tipo: {file_e_tipo[TIPO]}')
        
    return percorso_cartella,lista_files_tipi
        
if __name__ == "__main__":
    
    percorso_cartella = seleziona() # apre una finestra di selezione della cartella
    
    elenca(percorso_cartella,True)
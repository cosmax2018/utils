
# trim_line.py: taglia via la parte destra di ogni riga del file a partire dal carattere scelto.

from seleziona_file import seleziona

def modifica_file(nome_file,char):
    # Leggi il contenuto del file
    with open(nome_file, 'r', encoding='utf-8') as file:
        linee = file.readlines()

    print(linee)
    
    # Modifica ogni riga
    for i in range(len(linee)):
        if char in linee[i]:
            # Trova l'indice del carattere char
            indice_char = linee[i].index(char)
            
            # Taglia la parte destra a partire dal carattere €
            nuova_linea = linee[i][:indice_char].rstrip()

            # Aggiorna la lista delle linee
            linee[i] = nuova_linea + '\n'

    # Sovrascrivi il file con il testo modificato
    with open(nome_file, 'w', encoding='utf-8') as file_modificato:
        file_modificato.writelines(linee)


file_name = seleziona() # apre una finestra di selezione del file
    
if file_name:
    
    print("File selezionato:", file_name)
    
    modifica_file(file_name,'€')

import random
import string

def genera_file_casuale(nome_file, dimensione_kb):
    caratteri = string.ascii_letters + string.digits + string.punctuation + " \n"
    dimensione_byte = dimensione_kb * 1024

    with open(nome_file, 'w', encoding='utf-8') as f:
        for _ in range(dimensione_byte):
            f.write(random.choice(caratteri))

    print(f"File '{nome_file}' generato con successo ({dimensione_kb} KB).")

# Esempio d'uso
if __name__ == "__main__":
    nome_file = input("Nome del file da generare: ")
    dimensione_kb = int(input("Dimensione del file in KB: "))
    genera_file_casuale(nome_file, dimensione_kb)

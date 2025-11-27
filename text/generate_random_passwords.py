import sys,string
import random

alphabet = 'abc_def_ghi_lmn_opq_rst_uvz'
number_of_strings = 50_000_000
length_of_string = [20, 21, 22]

def generate_passwords(alphabet, num_strings, lengths):
    for _ in range(num_strings):
        random_length = random.choice(lengths)
        random_password = ''.join(random.choice(alphabet) for _ in range(random_length))
        yield random_password
        
def main(argv):

    # es.   py generate_random_passwords.py abc_def_ghi_lmn_opq_rst_uvz 50_000_000 20 22 passwords.txt
    #
    # n.b.: nella stringa dell'alfabeto, mettere '_' al posto degli spazi se no da errore !!
        
    alphabet = argv[0].replace('_',' ')
    number_of_strings = int(argv[1])
    length_of_string = [i for i in range(int(argv[2]),int(argv[3])+1)]
    print(f'alfabeto={alphabet}')
    print(f'quante stringhe generare={argv[1]}')
    print(f'lunghezze permesse delle stringhe={length_of_string}')
    
    passwords_generator = generate_passwords(alphabet, number_of_strings, length_of_string)
    
    with open(argv[4], 'w') as f:    
        for password in passwords_generator:
            print(password, end='\n', file=f)

if __name__ == "__main__":
    main(sys.argv[1:])  
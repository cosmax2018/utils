# ascii.py : programma per fornire i codici ascii dei caratteri di una stringa

s = input('Dammi la stringa da trasformare in ascii: ')

for c in s:
	print(hex(ord(c)).upper()[2:],end=',')

	

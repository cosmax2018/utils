
# invert_text.py : inverte un file di testo

f1 = open("file_da_invertire.txt", "r")
testo = f1.readlines()

f2 = open("file_invertito.txt","w")

for riga in reversed(testo):
	f2.write(riga)
	print(riga)

f2.close()

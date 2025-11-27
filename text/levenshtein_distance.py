#
# distanza di Levenshtein written in Python
#
#	(c) Copyright 2019 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)
#
# Nella teoria dell'informazione e nella teoria dei linguaggi, la distanza di Levenshtein,
# o distanza di edit, è una misura per la differenza fra due stringhe. Introdotta dallo 
# scienziato russo Vladimir Levenshtein nel 1965[1], serve a determinare quanto due stringhe
# siano simili. Viene applicata per esempio per semplici algoritmi di controllo ortografico 
# e per fare ricerca di similarità tra immagini, suoni, testi, etc.
# La distanza di Levenshtein tra due stringhe A e B è il numero minimo di modifiche elementari
# che consentono di trasformare la A nella B. Per modifica elementare si intende.
#
# la cancellazione di un carattere,
# la sostituzione di un carattere con un altro, o
# l'inserimento di un carattere.

def minimum(a,b,c):
	min = a
	if min > b:
		min = b
	if min > c:
		min = c
	return min

def levenshteinDistance(x,y):
    m = len(x)
    n = len(y)
    prev = [0]*(n+1)
    curr = [0]*(n+1)
    tmp = 0
 
    for i in range(0,n+1):
        prev[i] = i
 
    for i in range(1,m+1):
        curr[0] = i
        for j in range(1,n+1):
            if x[i-1] != y[j-1]:
                k = minimum(curr[j-1],prev[j-1],prev[j])
                curr[j]=k+1
            else:
                curr[j]=prev[j-1]
        tmp = prev
        prev = curr
        curr = tmp
 
    distance = prev[n]
 
	#libero la memoria usata
    curr = []
    prev = []
 
    return distance

# def main():
	# print ("per calcolare la distanza ho bisogno di due stringhe")
	# print ()
	# a = input ("dammi la prima stringa : ")
	# b = input ("dammi la seconda stringa : ")
	# print ()
	# print ("Levenshtein distance between " + str(a) + " and " + str(b) + " is : " + str(levenshteinDistance(a,b)))
	
# main()
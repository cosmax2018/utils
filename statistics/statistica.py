
# statistics.py libreria di statistica

import math
import itertools
	
def calcMax(s):
	# ritorna il valore massimo di una lista
	if len(s) == 0:
		return None
	m = s[0]
	for e in s[1:]:
		if e > m:
			m = e
	return m
	
def calcModa(x):
	# calcolo della moda
	freq = dict()
	for e in x:
		freq[e] = freq.get(e,0)+1
	max_freq = calcMax(list(freq.values()))
	moda = []
	for e in freq:
		if freq[e] == max_freq:
			moda.append(e)
	return moda
	
def calcMedia(x):
	# calcolo della media aritmetica dei valori del vettore x
	return sum(x)/len(x)
	
def calcVarianza(x):
	# calcola la somma delle differenze al quadrato dei valori del vettore x rispetto alla media
	m = calcMedia(x)
	d = 0 
	for v in x:
		d += (v-m)*(v-m)
	return d/len(x)

def calcDeviazioneStardard(x):
	# calcola lo squarto quadratico medio
	return calcVarianza(x)**0.5

def calcFreqMedia(x):
	# calcolo della media delle occorrenze di una data variabile
	s = 0
	d = 0		# distanza fra gli '1' ossia fra le occorrenze
	n = len(x)
	k = 0		# numero di valori
	for i in range(n):
		if x[i] == 1:
			d += 1
			s += d
			k += 1
			d = 0
		else:
			d += 1
	if k == 0:
		return None
	return s/k
			
def calcFreqVarianza(x,m):
	# calcolo della varianza d elle occorrenze di una data variabile
	s = 0
	d = 0		# distanza fra gli '1' ossia fra le occorrenze
	n = len(x)
	k = 0		# numero di valori
	for i in range(n):
		if x[i] == 1:
			d += 1
			s += (d-m)*(d-m)
			k += 1
			d = 0
		else:
			d += 1
	if k == 0:
		return m,None			
	return m,s/k

	
def permutations(set,k):
	# e.g.:
    # 	lst = permutations( "ABCDE", 3 )
    return list(itertools.permutations(set,k))
	
def combinations(set,k):
	# e.g.:
    # 	lst = combinations( "ABCDE", 3 )
    return list(itertools.combinations(set,k))
	
def combinations_with_replacement(set,k):
	# e.g.:
    # 	lst = combinations_with_replacement( "ABCDE", 3 )
    return list(itertools.combinations_with_replacement(set,k))

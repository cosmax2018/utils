#
# routines per i numeri primi
#
#import keyboard
from math import sqrt

def nonPrimeProof(n):
	# scomposizione in fattori
	for i in range(1,n):
		for j in range(1,n):
			if n == i*j:
				return (i,j)

def isPrime(n):
    # testa se il numero n è primo oppure no
	for i in range(2,int(sqrt(n))+1): #..più veloce di range(2,n-1)!
		if n % i == 0:
			return False
	return True

def crivello(n):
	# implementa l'algoritmo di Eratostene per cercare i numeri primi fino a 'n'
	cell = [0]*n
	for i in range(2,n):
		if cell[i] == 0:
			for j in range(2*i,n,i):
				cell[j] = 1
				
	# conta le caselle che corrispondono ai numeri primi
	count = 0
	primes = []
	for i in range(2,n):
		if cell[i] == 0:
			count += 1
			primes.append(i)
	return [count,primes]
	
def findPrime(n):
	# cerca i primi 'n' numeri primi
	count = 4			# comincio dal quarto numero primo
	primes = [1,2,3]	# in quanto i primi tre sono 1,2 e 3
	i = 5				# quindi testo se 5 è primo..
	while count <= n:
		if isPrime(i):
			#if keyboard.is_pressed('space'):
			#    print(count)   
			primes.append(i) # ho trovato che 'i' è un numero primo
			count += 1
		i += 2 				 # ..solo i numeri dispari possono essere primi.
	return primes
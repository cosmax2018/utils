
# individual.py : simple GA v.2 written in Python (slow version)
#
#	(c) Copyright 2020-21 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

from random import choice, randint

class Individual():
	# classe di inizializzazione o costruttore
	def __init__(self,alphabet,chromosomeLength,objectiveFunction):
		self.alphabet			= alphabet			# alfabeto
		self.chromosomeLength	= chromosomeLength	# length of the individual
		self.objectiveFunction	= objectiveFunction	# funzione obiettivo utilizzata per il calcolo della fitness

		self.fitness			= 0					# la fitness
		self.chromosome			= []				# il cromosoma dell'individuo
		
	def getChromosome(self,i):	return self.cromosome[i]								# restituisce il gene i-esimo

	def setChromosome(self,i,v):self.cromosome[i] = v									# setta il gene i-esimo
	
	def getChromosomes(self):	return self.chromosome									# restituisce tutti i geni
	
	def setChromosomes(self,v):	self.chromosome = v										# setta tutti i geni
	
	def getFitness(self):		return self.fitness										# restituisce la fitness
	
	def setFitness(self):		self.fitness = self.objectiveFunction(self.chromosome)	# calcola la fitness

	def rndChromosome(self):
		# genera un individuo a caso
		self.cromosome = []
		for i in range(self.chromosomeLength):
			self.chromosome.append(choice(self.alphabet))
	
	def mutateChromosome(self):	self.chromosome[randint(0,self.chromosomeLength-1)] = choice(self.alphabet) 	# genera una mutazione casuale
	
	def crossoverChromosomes(self,parent):
		# incrocia i cromosomi di due individui ottenendo altri due cromosomi figli
		child1,child2 = [],[]
		crossOverPoint = randint(1,self.chromosomeLength-1)
		for i in range(self.chromosomeLength):
			if i < crossOverPoint:
				child1.append(self.chromosome[i])
				child2.append(parent.chromosome[i])
			else:
				child1.append(parent.chromosome[i])
				child2.append(self.chromosome[i])
		return (child1,child2)
	
	def printFitness(self):
		# stampa la fitness
		print('%5f '%self.fitness,end=' - ')
		
	def printChromosome(self):
		# stampa il cromosoma
		for i in range(self.chromosomeLength):
			print(self.chromosome[i],end='')
		print()
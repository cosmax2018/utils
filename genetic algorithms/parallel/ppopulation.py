
# ppopulation.py : simple parallel GA v.2 written in Python (slow version)

#	(c) Copyright 2020 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

import sys,random,time,itertools

from pindividual import pIndividual


from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()	

class pPopulation():

	def __init__(self,populationSize,tournamentSize,mutationRate,alphabet,chromosomeLength,objectiveFunction):
		self.populationSize		= populationSize			# dimensione della popolazione
		self.tournamentSize		= tournamentSize			# dimensione della selezione
		self.mutationRate		= mutationRate				# rateo di mutazione
		self.alphabet 			= alphabet					# alfabeto su cui si basano i cromosomi
		self.chromosomeLength	= chromosomeLength			# lunghezza dei cromosomi
		self.objectiveFunction	= objectiveFunction			# la funzione obiettivo
		
		self.individuals = []								# la popolazione di individui

	data_individuals = None						# scattered data
		
	def randomize(self): random.seed(time.time())
		
	def initializePopulation(self):
		# crea una popolazione di individui
		self.randomize()
		d = []
		k = int(self.populationSize/size)
		j = 0
		if rank == 0:
			for i in range(self.populationSize):
				self.individuals.append(pIndividual(self.alphabet,self.chromosomeLength,self.objectiveFunction)) # istanzia un nuovo individuo
				j += 1
				if j < k:
					d.append(self.individuals[i:i+k])
				else:
					j = 0

			data_individuals = [d[x] for x in range(size)]	# data to scatter
		else:
			data_individuals = None

		data_individuals = comm.scatter(data_individuals, root=0)	# on every node scatter data

	def getPopulation(self,i):	
		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data
		if rank == 0:
			return self.individuals[i]	# restituisce l'individuo i-esimo
	
	def setPopulation(self,i,v):
		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data

		if rank == 0:
			self.individuals[i] = v		# setta l'individuo i-esimo

		data_individuals = comm.scatter(data_individuals, root=0)	# on every node scatter data

	def rndPopulation(self):
		# genera una popolazione casuale di individui dal cromosoma generato a caso
		for individual in data_individuals:
			individual.rndChromosome()

	def evaluatePopulation(self):
		# valuta la popolazione di individui
		for individual in data_individuals:
			individual.setFitness()
			
	def sortPopulation(self):
		# ordina la popolazione in base alla fitness
		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data

		if rank == 0:
			for i,j in itertools.product(range(self.populationSize),range(self.populationSize)):
				if self.individuals[i].getFitness() > self.individuals[j].getFitness():
					self.individuals[i],self.individuals[j] = self.individuals[j],self.individuals[i]

			d = []
			for i in range(self.populationSize):
				if i % size == 0:
					d.append(self.individuals[i:i+size])

			data_individuals = [d[x] for x in range(0,size)]	# data to scatter
		else:
			data_individuals = None			

		data_individuals = comm.scatter(data_individuals, root=0)	# on every node scatter data
				
	def mutatePopulation(self):
		# genera delle mutazioni casuali in alcuni individui della popolazione
		for individual in data_individuals:
			if random.random() < self.mutationRate:
				individual.mutateChromosome()
				
	def evolvePopulation(self):
		# fa un passo evolutivo incrociando i migliori individui a 2 a 2
		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data

		if rank == 0:
			for i in range(0,self.tournamentSize,2):
				child1,child2 = self.individuals[i].crossoverChromosomes(self.individuals[i+1])
				self.individuals[self.populationSize-i-1].setChromosomes(child1)
				self.individuals[self.populationSize-i-2].setChromosomes(child2)
			
			d = []
			for i in range(self.populationSize):
				if i % size == 0:
					d.append(self.individuals[i:i+size])

			data_individuals = [d[x] for x in range(0,size)]	# data to scatter
		else:
			data_individuals = None			

		data_individuals = comm.scatter(data_individuals, root=0)	# on every node scatter data				
			
	def replaceWhorst(self,threshold):
		# rimpiazza i peggiori individui della popolazione con altrettanti individui generati a caso

		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data

		if rank == 0:
			for individual in self.individuals:
				if individual.getFitness() < threshold:
					individual.rndChromosome()
			d = []
			for i in range(self.populationSize):
				if i % size == 0:
					d.append(self.individuals[i:i+size])

			data_individuals = [d[x] for x in range(0,size)]	# data to scatter
		else:
			data_individuals = None			

		data_individuals = comm.scatter(data_individuals, root=0)	# on every node scatter data	
				
	def getResults(self):
		# ritorna la miglior fitness e il miglior individuo della popolazione
		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data
		if rank == 0:
			return (self.individuals[0].getFitness(),self.individuals[0].getChromosomes())

	def savePopulation(self,file_name):
		# salva su file la popolazione
		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data
		if rank == 0:
			import pickle
			with open(file_name, "wb") as fp:
				pickle.dump(self.individuals, fp)
			
	def loadPopulation(self,file_name):
		# carica da file la popolazione
		if rank == 0:
			import pickle
			with open(file_name, "rb") as fp:
				self.individuals = pickle.load(fp)
		
			d = []
			for i in range(self.populationSize):
				if i % size == 0:
					d.append(self.individuals[i:i+size])

			data_individuals = [d[x] for x in range(0,size)]	# data to scatter
		else:
			data_individuals = None			

		data_individuals = comm.scatter(data_individuals, root=0)	# on every node scatter data
			
	def printPopulation(self, n=None):
		# stampa dell'intera popolazione di individui o di una sua parte
		self.individuals = comm.gather(data_individuals, root=0)	# from every node gather data
		if rank == 0:		
			print()
			print("\033[2;1H")
			i = 0
			if n == None:
				for individual in self.individuals:
					print('%3d '%i,end=" - ")
					individual.printFitness()
					individual.printChromosome()
					i += 1
			else:
				for individual in self.individuals:
					print('%3d '%i,end=" - ")
					individual.printFitness()
					individual.printChromosome()
					if i < n:
						i += 1
					else:
						break
	


# population_multiprocessing.py : simple GA v.2 written in Python (slow version)
#
#	(c) Copyright 2021 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

from multiprocessing import Pool
import random, time, itertools

from individual import Individual

NUMERO_DI_PROCESSI = 4		# è uguale al numero di cores logici della macchina

class Population():

	def __init__(self,populationSize,tournamentSize,mutationRate,alphabet,chromosomeLength,objectiveFunction):
		# classe di inizializzazione o costruttore
		self.numberOfProcesses	= NUMERO_DI_PROCESSI #int(populationSize/NUMBER_OF_INDIVIDUALS_PER_PROCESS)	# numero di processi necessari
		
		self.populationSize		= populationSize			# dimensione della popolazione
		self.tournamentSize		= tournamentSize			# dimensione della selezione
		self.mutationRate		= mutationRate				# rateo di mutazione
		self.alphabet 			= alphabet					# alfabeto su cui si basano i cromosomi
		self.chromosomeLength	= chromosomeLength			# lunghezza dei cromosomi
		self.objectiveFunction	= objectiveFunction			# la funzione obiettivo
		
		self.individuals = []								# la popolazione di individui

		self.randomize()
		for i in range(self.populationSize):
			self.individuals.append(Individual(self.alphabet,self.chromosomeLength,self.objectiveFunction)) # istanzia un nuovo individuo
			
	def randomize(self): random.seed(time.time())
			
	def getPopulation(self,i):		return self.individuals[i]	# restituisce l'individuo i-esimo
	
	def setPopulation(self,i,v):	self.individuals[i] = v		# setta l'individuo i-esimo
	
	def rndPopulation(self):
		# genera una popolazione casuale di individui dal cromosoma generato a caso
		for individual in self.individuals:
			individual.rndChromosome()
	
	def dividi_in_blocchi(self,nproc):
		# suddivide in SUB_DIM blocchi di dimensione da processare in parallelo.
		SUB_DIM = int(self.populationSize/nproc)
		blocks = []
		for i in range(nproc):
			blocks.append( self.individuals[i*SUB_DIM:(i+1)*SUB_DIM] )
			# print('appendo gli individui da: ',i*SUB_DIM,(i+1)*SUB_DIM)
		return tuple(blocks)
		
	def ricombina_i_blocchi(self,blocks):
		numblocks = len(blocks)
		#print("Numero di blocchi da ricomporre: {0}".format(numblocks))
		self.individuals = []
		for i in range(numblocks):
			for row in blocks[i]:
				self.individuals.append(row)
		
	def evaluation_worker(self,individuals):
		for individual in individuals:
			individual.setFitness()
		return individuals
			
	def evaluatePopulation(self):
		# valuta la popolazione di individui
		# possiamo suddividere gli individui in gruppi di NUMBER_OF_INDIVIDUALS_PER_PROCESS
		# da dare a differenti processi.
		
		BLOCKS = self.dividi_in_blocchi(NUMERO_DI_PROCESSI)
		with Pool(processes = NUMERO_DI_PROCESSI) as p:
			results = p.map(self.evaluation_worker,BLOCKS)#,chunksize=len(BLOCK))
			p.close()
			p.join()
			
		self.ricombina_i_blocchi(results)
			
	def sortPopulation(self):
		# ordina la popolazione in base alla fitness
		for i,j in itertools.product(range(self.populationSize),range(self.populationSize)):
			if self.individuals[i].getFitness() > self.individuals[j].getFitness():
				self.individuals[i],self.individuals[j] = self.individuals[j],self.individuals[i]
				
	def mutatePopulation(self):
		# genera delle mutazioni casuali in alcuni individui della popolazione
		for individual in self.individuals:
			if random.random() < self.mutationRate:
				individual.mutateChromosome()
			
	def evolving_thread(self,individual1,individual2,individual3,individual4):
		child1,child2 = individual1.crossoverChromosomes(individual2)
		individual3.setChromosomes(child1)
		individual4.setChromosomes(child2)
		
	def evolvePopulation(self):
		# fa un passo evolutivo incrociando i migliori individui a 2 a 2
		for i in range(0,self.tournamentSize,2):
			child1,child2 = self.individuals[i].crossoverChromosomes(self.individuals[i+1])
			self.individuals[self.populationSize-i-1].setChromosomes(child1)
			self.individuals[self.populationSize-i-2].setChromosomes(child2)
			
	def replaceWhorst(self,threshold):
		# rimpiazza i peggiori individui della popolazione con altrettanti individui generati a caso
		for individual in self.individuals:
			if individual.getFitness() < threshold:
				individual.rndChromosome()
				
	def getResults(self):
		# ritorna la miglior fitness e il miglior individuo della popolazione
		return (self.individuals[0].getFitness(),self.individuals[0].getChromosomes())

	def savePopulation(self,file_name):
		# salva su file la popolazione
		import pickle
		with open(file_name, "wb") as fp:
			pickle.dump(self.individuals, fp)
			
	def loadPopulation(self,file_name):
		# carica da file la popolazione
		import pickle
		with open(file_name, "rb") as fp:
			self.individuals = pickle.load(fp)
			
	def printPopulation(self, n=None):
		# stampa dell'intera popolazione di individui o di una sua parte
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
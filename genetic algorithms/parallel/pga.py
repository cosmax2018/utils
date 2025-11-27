
# pga.py : simple parallel GA v.2 written in Python (slow version)

#	(c) Copyright 2020 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

import threading

from ppopulation import pPopulation					# parallel version
# from population_multithreads import Population	# multi-threads version.

class Simple_PGA:

	def __init__(self,populationSize, tournamentSize, mutationRate, alphabet, chromosomeLength, objectiveFunction):
		self.populationSize		= populationSize
		self.tournamentSize		= tournamentSize
		self.mutationRate		= mutationRate
		self.alphabet 			= alphabet
		self.chromosomeLength	= chromosomeLength
		self.objectiveFunction	= objectiveFunction
		
		self.population			= pPopulation(populationSize,tournamentSize,mutationRate,alphabet,chromosomeLength,objectiveFunction)	# una popolazione di individui

	def getResults(self):				return self.population.getResults()
	
	def savePopulation(self,file_name):	return self.population.savePopulation(file_name)	
	
	def loadPopulation(self,file_name):	return self.population.loadPopulation(file_name)
	
	def replaceWhorst(self,threshold):	return self.population.replaceWhorst(threshold)
	
	def initializePopulation(self):		return self.population.initializePopulation()
	
	def newRndPopulation(self):			return self.population.rndPopulation()
	
	def sortPopulation(self):			return self.population.sortPopulation()
	
	def evaluatePopulation(self):		return self.population.evaluatePopulation()
	
	def mutatePopulation(self):			return self.population.mutatePopulation()
	
	def evolvePopulation(self):			return self.population.evolvePopulation()
	
	def printPopulation(self,n=None):	return self.population.printPopulation(n)
	
	#
	
	def evaluate_thread(self):			self.population.evaluatePopulation()	# evaluating population fitness
	
	def sort_thread(self):				self.population.sortPopulation()		# sorting population by fitness
	
	def evolve_thread(self):			self.population.evolvePopulation()		# evolving population
	
	def mutate_thread(self):			self.population.mutatePopulation()		# mutating population

	#		
	# def stepGA(self):
		# esegue l'algoritmo ad uno step alla volta
		# self.population.evaluatePopulation()

		# self.population.sortPopulation()

		# self.population.evolvePopulation()

		# self.population.mutatePopulation()

	def stepGa_multiThreads(self):
		#esegue l'algoritmo ad uno step alla volta in modalità multi-threads
		threads = []
		
		thread_evaluate = threading.Thread(target=self.evaluate_thread)
		threads.append(thread_evaluate)
		thread_evaluate.start()
		
		thread_sort = threading.Thread(target=self.sort_thread)
		threads.append(thread_sort)
		thread_sort.start()
		
		thread_evolve = threading.Thread(target=self.evolve_thread)
		threads.append(thread_evolve)
		thread_evolve.start()
		
		thread_mutate = threading.Thread(target=self.mutate_thread)
		threads.append(thread_mutate)
		thread_mutate.start()
		
		for thread in threads:
			thread.join()			
		
	def runGa(self, maxIterations, threshold=0, m=20):
		# esegue l'algoritmo genetico
		
		print("\033[1;1HITERATION: ")
		
		# the iterations
		for iterations in range(maxIterations):
			
			print("\033[1;12H" + str(iterations))
			
			self.stepGa()
			
			self.population.printPopulation(m)		 	# stampa i primi m individui della popolazione
			
			if iterations % 100 == 0:	# ogni 100 iterazioni rimpiazza gli individui con fitness < fitness minima (Es threshold = 30) con nuovi individui creati a caso
				if threshold != 0:
					self.population.replaceWhorst(threshold)
					

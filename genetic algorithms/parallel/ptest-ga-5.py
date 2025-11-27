
# ptest-ga-5.py : esegue degli esempi utilizzando la libreria sugli algoritmi genetici parallela

#	(c) Copyright 2020 by ....@_°° Lumachina SW
#    Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

import time,sys,random
import itertools
from PIL import Image

from init_lib import *														# versione lenta
add_path_to_lib('genetic algorithms')
add_path_to_lib('graphics')
from pga import Simple_PGA													# simple parallel genetic algorithms
from images import SuperImposeNewRectangleRGBA,ColourDistanceSquaredRGBA	# graphics

def randomize(): random.seed(time.time())

def decodeImage_test(individual,canvas_dim):
	# decodifica l'immagine originariamente presente in individual ora trasformato in un vettore di numeri x
	prev_image = Image.new('RGBA',canvas_dim)
	for i in range(0,len(individual),M):				# ciclo sui numeri che servono per definire tutti i rettangoli
		v = individual[i:i+M]							# M numeri interi che mi servono per definire un rettangolo
		# color = (v[0]%256,v[1]%256,v[2]%256,v[3]%256)	# colore R,G,B,A
		# rect = ((v[4],v[5]),(v[6],v[7]))				# ((x1,y1),(x2,y2))
		color = (v[0]%256,v[1]%256,v[2]%256,128)		# colore R,G,B,A e canale alfa A = 128 (trasparenza 50%)
		rect = ((v[3],v[4]),(v[5],v[6]))				# ((x1,y1),(x2,y2))
		image,rect = SuperImposeNewRectangleRGBA(prev_image,rect,color,canvas_dim)
		prev_image = image
	return prev_image
	
def fitness_test(individual,image_target):
	# utilizzando il metodo ColourDistanceSquared della libreria images.py
	# calcola quanto 'fitta' un immagine rispetto a un altra
	# la distanza di colore al quadrato varia fra i valori 8064.6 (=MIN_FITNESS) e 40704.5 (=MAX_FITNESS)
	# se l'immagine di riferimento (target) ha una trasparenza nulla 0% (A = 255)
	# e se l'immagine che approssima il target ha una trasparenza del 50% (A = 128)
	
	test_image = decodeImage_test(individual,(XRES,YRES))
	pixels = test_image.load()	# le due immagini devono avere la stessa dimensione!
	
	F = 0.0	# somma delle distanze
	
	for x,y in itertools.product(range(XRES),range(YRES)):
		F += (MAX_FITNESS - ColourDistanceSquaredRGBA(pixels[x,y],pixels_target[x,y]))/FITNESS_DIFF
				
	return F/AREA	# divido per il numero di punti contenuti nell'area dell'immagine per fare una media delle fitness
	
def objective_test(individual):
	# calcola la fitness rispetto all'obiettivo
	return fitness_test(individual,image_target)
	
def main(argv):			  
	#						n.rettangoli n.iteraz. 	pop size	tournament	mutation	replace		print
	#		py test-ga-5.py 	100 	  50000 		100 		6 			0.25	0			0
	#		py test-ga-5.py 	50 		100000 			100			8 			0.25	0			0
	# 		py test-ga-5.py 100 50000 100 6 0.25 0 0
	#		py test-ga-5.py 200 100000 100 6 0.25 0 0
	randomize()
	
	global workDir, targetPicture
	workDir 		= '/home/massimiliano/python/genetic algorithms/images/'	# (a lavoro)
	targetPicture	= 'Monnalisa_128x170'
	
	try:
		numeroRettangoli	= int(argv[0])	# numero di rettangoli utilizzati per l'approssimazione
		maxIterations		= int(argv[1])	# numero massimo di iterazioni/generazioni
		populationSize		= int(argv[2])  # dimensione della popolazione
		tournamentSize		= int(argv[3])  # numero di partecipanti alla selezione
		mutationRate		= float(argv[4])# rateo di mutazione
		threshold			= float(argv[5])# soglia sotto la quale sostituisc2 gli individui peggiori con nuovi individui (se zero non fa nulla!)
		m 					= int(argv[6])	# stampa i primi m individui della popolazione
	except IndexError:
		numeroRettangoli= 100
		maxIterations	= 1000
		populationSize	= 50
		tournamentSize	= 6
		mutationRate	= 0.25
		threshold		= 0
		m				= 20
	finally:
		print(f'Numero di rettangoli utilizzati: {numeroRettangoli}')
		print(f'Numero massimo di iterazioni: {maxIterations}')
		print(f'Dimensione della popolazione: {populationSize}')
		print(f'Dimensione della selezione: {tournamentSize}')
		print(f'Rateo di mutazione: {mutationRate}')
		if threshold != 0:
			print(f'Rimpiazza i peggiori sotto la soglia: {threshold}')
		
	#test 5 - approssimazione di una immagine con 50 rettangoli (ognuno dei quali ha bisogno di 64 bits per essere definito)
	
	global MAX_FITNESS,MIN_FITNESS,FITNESS_DIFF
	MAX_FITNESS = 40704.5 #65025
	MIN_FITNESS = 8064.5
	FITNESS_DIFF = MAX_FITNESS-MIN_FITNESS
	
	global NUMERO_DI_RETTANGOLI
	NUMERO_DI_RETTANGOLI = numeroRettangoli						# numero di rettangoli impiegati
	
	global M
	M				= 7											# numeri che mi servono per definire un rettangolo
	alphabet 		= [i for i in range(255)]					# sistema piu furbo...
	chromosomeLength = M * NUMERO_DI_RETTANGOLI					# mi servono M numeri per ogni rettangolo da disegnare
	
	global image_target, pixels_target
	image_target = Image.open(workDir + targetPicture + '.png') # carica l'immagine target
	image_target.putalpha(255)									# aggiunge/sovrascrive il canale alfa della trasparenza con valore 255 (opaco al 100%)
	pixels_target = image_target.load()							# carica i pixels dell'immagine target
	
	global XRES,YRES,AREA
	XRES,YRES = image_target.size
	AREA = XRES*YRES
	
	# initialize GA:
	simple_pga = Simple_PGA(populationSize, tournamentSize, mutationRate, alphabet, chromosomeLength, objective_test)
	
	simple_pga.initializePopulation()	# inizializza la popolazione

	simple_pga.newRndPopulation()		# genera gli individui casualmente

	iterations	= [i for i in range(maxIterations)]			# asse X
	bestFitness	= [0 for i in range(maxIterations)]			# asse Y (fitness)

	# iterate :
	for iteration in iterations:
		
		t = time.time()
		
		simple_pga.stepGa()	# fai una iterazione
		
		bestFitness[iteration],bestIndividual = simple_pga.getResults()
		
		dt = time.time() - t
		
		print(f'ITERATION N.{iteration} Best Fitness is {bestFitness[iteration]} Time elapsed is {int(dt)} sec.')
		
		# ogni tot. iterazioni salva l'immagine che approssima nella maniera migliore l'immagine target e rimpiazza i peggiori individui
		if iteration % 100 == 0:

			image = decodeImage_test(bestIndividual,(XRES,YRES))
			image.save(workDir + targetPicture + '-ITER_'+str(iteration)+'-POP_'+str(populationSize)+'-RECT_'+str(NUMERO_DI_RETTANGOLI)+'-FITNESS_'+str(int(10000*bestFitness[iteration])/100)+'.png')
			
			simple_pga.savePopulation(workDir + 'population' + '-ITER_'+str(iteration) + '.txt')
			
			if threshold != 0:
				simple_pga.replaceWhorst(threshold)

if __name__ == "__main__":
	main(sys.argv[1:])

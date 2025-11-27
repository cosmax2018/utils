
# neuron.py : implementazione di un neurone in Python utilizzando NumPy
#             (attenzione: risulta piu' lento del metodo tradizionale)
#
# CopyRight 2021-2022 by Lumachina Software - @_°° 
# Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

import math, random, time

import numpy as np

INPUT,OUTPUT = 0,1

def timer(function):						# prende come parametro la funzione di cui misurare il tempo di esecuzione
	def timed(*args):						# args sono i parametri passati alla funzione da misurare
		start_time = time.time()			# Ti
		result = function(*args)			# esegue la funzione
		elapsed = time.time() - start_time	# Tf-Ti
		print('Function "{name}" took {time} seconds to complete.'.format(name=function.__name__, time=elapsed))
		return result						# restituisce il risultato dell'esecuzione della funzione
	return timed

class Neuron():
	
	def __init__(self,number_of_inputs,		\
					  learning_rate = None,	\
					  dataset = None,		\
					  iterazioni = None):
					  
		if dataset != None:
			self.dataset = dataset				# il dataset che serve per l'addestramento del neurone
			
		if iterazioni != None:
			self.iterazioni = iterazioni		# quanti cicli di apprendimento ?
			
		if learning_rate != None:
			self.learning_rate = learning_rate	# rateo di apprendimento
			self.affidabilita = 0				# quanto è affidabile l'apprendimento con gli attuali pesi e bias relativamente al dataset
			
		self.index = 0
		self.number_of_inputs = number_of_inputs
		
		self.inputs = None 		# gli inputs del neurone
		self.output = 0			# l'output del neurone
		
		self.input = None 		# l'input dal dataset
		self.output_atteso = 0	# l'output dal dataset
		
		self.weights = None		# i pesi
		self.bias = 0.0			# il bias
		
		self.delta = 0.0		# errore delta usato per la backpropagation
		
	def reset(self):
		# resetta il neurone ( da chiamare sempre prima di fare il training )
		random.seed(time.time())
		self.inputs, self.output = np.zeros(self.number_of_inputs),0
		self.weights = np.random.uniform(-1,1,self.number_of_inputs)
		self.bias = random.uniform(-1,1)
		self.delta = 0.0
		
	def fire(self, inputs = None):
		# calcola il valore di uscita in base a quelli di ingresso e ai relativi pesi delle connessioni
		if inputs != None:
			if len(inputs) == self.number_of_inputs:
				self.inputs = inputs
			else:
				print('neuron::fire(): length of inputs incorrect!')
				self.output = None
				return None
		try:
			z = 0
			for (input,weight) in zip(self.inputs,self.weights):
				z += input * weight
			self.output = z + self.bias
			return self.output
		except TypeError:
			print(f'neuron::fire():Error! Inputs: {self.inputs}')
			print(f'neuron::fire():Error! Weights: {self.weights}')
	
	def sigmoide(self,x):
		# restituisce un valore compreso fra 0 e 1
		# dato che i neuroni o sparano o non sparano
		# cioè funzionano in modo binario 0/1
		# allora devo trasformare il mio input z "analogico"
		# in digitale con la funzione sigmoide.
		if x < -700:
			return 0
		else:
			return 1/(1+math.exp(-x))
	
	def sigmoide_p(self,t):
		return self.sigmoide(t)*(1-self.sigmoide(t))

	def get_index(self):
		# ritorna l'indice numerico progressivo associato al neurone facente parte del layer
		return self.index

	def get_number_of_inputs(self):
		return self.number_of_inputs
		
	def get_inputs(self):
		# ritorna i valori degli inputs del neurone
		return tuple(self.inputs)
	
	def get_input(self,i):
		# ritorna l'i-esimo input del neurone
		try:
			return self.inputs[i]
		except IndexError:
			print('neuron.py::get_input:indice fuori dai limiti.')
			return None
			
	def get_output(self):
		# ritorna il valore dell'output del neurone
		return self.output
	
	def get_sigmoid_output(self):
		# ritorna il valore normalizzato fra 0 e 1 dell'output del neurone
		return self.sigmoide(self.output)
		
	def get_sigmoid_p_output(self):
		# ritorna la derivata
		return self.sigmoide_p(self.output)
		
	def get_weights(self):
		return tuple(self.weights)
		
	def get_weight(self,i):
		# ritorna il peso della connessione dell'input i-esimo del neurone
		try:
			return self.weights[i]
		except IndexError:
			print('neuron.py::get_weight:indice fuori dai limiti.')
			return None
			
	def get_bias(self):
		return self.bias
		
	def get_affidabilita(self):
		# ritorna la percentuale di risultati corretti
		return self.affidabilita
		
	def get_delta(self):
		# ritorna il delta dell'errore per il neurone
		return self.delta
		
	def set_weights(self,weights):
		# setta i pesi del neurone
		self.weights = weights
			
	def set_bias(self,bias):
		#setta il bias del neurone
		self.bias = bias

	def set_delta(self,delta):
		# setta il delta dell'errore per il neurone
		self.delta = delta
				
	def update_weight_and_bias_by_delta(self):
		# aggiorna i pesi e il bias in base al delta del neurone
		for i,input in enumerate(self.inputs):
			self.weights[i] += self.learning_rate*self.delta*input
		self.bias += self.learning_rate*self.delta
		
	def forward_update_weight_and_bias(self,output_effettivo):
		# forward propagation of the errors
		
		costo = (output_effettivo - self.output_atteso)**2
		
		# derivate parziali e calcolo dei pesi e del bias
		derivata_costo_rispetto_output_effettivo = 2*(output_effettivo - self.output_atteso)
		derivata_output_effettivo_rispetto_z = self.sigmoide_p(self.output)
		
		derivata_z_rispetto_w = []
		
		for i in range(self.number_of_inputs):
			derivata_z_rispetto_w.append(self.input[i])
		
		derivata_z_rispetto_b = 1
		
		derivata_costo_z = derivata_costo_rispetto_output_effettivo * derivata_output_effettivo_rispetto_z
		
		derivata_costo_rispetto_w = []
		
		for i in range(self.number_of_inputs):
			derivata_costo_rispetto_w.append(derivata_costo_z * derivata_z_rispetto_w[i])
		
		derivata_costo_rispetto_b = derivata_costo_z * derivata_z_rispetto_b
		
		# aggiorna i pesi e il bias
		for i in range(self.number_of_inputs):
			self.weights[i] = self.weights[i] - self.learning_rate * derivata_costo_rispetto_w[i]
		
		self.bias = self.bias - self.learning_rate * derivata_costo_rispetto_b	
		
	def training_step(self):
		# uno step di training
		choice = random.randint(0,len(self.dataset[0])-1)
		self.input = self.dataset[INPUT][choice]			# prende un input a caso dal dataset
		self.output_atteso = self.dataset[OUTPUT][choice]	# prende il relativo output atteso
			
		self.fire()											# spara il neurone!
		
		#										 output effettivo
		self.forward_update_weight_and_bias(self.sigmoide(self.output))
		
	@timer
	def training(self):
		# addestramento: calcola i pesi e il bias del neurone
		# quanti pesi devo considerare?  devono essere tanti quanti sono gli inputs...
		# dataset è composto da un certo numero di n-tuple così fatte: (i0,i1,i2,...,in,output)
		# per cui prendo la prima n-tupla che è uguale alle altre ne calcolo la dimensione
		# diffatti l'ultimo valore della n-tupla è l'output e non lo devo considerare
		
		# self.reset()
		
		for iterazione in range(self.iterazioni):
			self.training_step()					# un passo di addestramento
		
	def test(self,verbose=False):
		# testa l'apprendimento sul dataset usato per l'addestramento e stampa i risultati
		risultato_corretto = 0
		for i,input in enumerate(self.dataset[INPUT]):
			output_atteso = self.dataset[OUTPUT][i]		# prende l'output
			output_effettivo = self.fire(input)			# prende la output_effettivo della rete addestrata
			
			if output_effettivo > 0.5:
				if output_atteso == 1:
					if verbose: print(input,'--> 1')
					risultato_corretto += 1
				else:
					print(input,'-->1 (!output_effettivo errata!)')
			elif output_effettivo <= 0.5:
				if output_atteso == 0:
					if verbose: print(input,'--> 0')
					risultato_corretto += 1
				else:
					print(input,'-->0 (!output_effettivo errata!)')
					
		self.affidabilita = 100*risultato_corretto/len(self.dataset[0])
		print(f'\noutput_effettivo affidabile nel {self.affidabilita} % dei casi\n')

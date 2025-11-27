
# neural-network.py : implementazione di una rete neurale composta da strati di neuroni in Python
#
# CopyRight 2021 by Lumachina Software - @_°° 
# Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

from neurons import Neurons

import random,time,pickle

INPUT,OUTPUT = 0,1

class NeuralNetwork():

	def __init__(self,dataset,						\
					  iterazioni,					\
					  learning_rate, 				\
					  number_of_neurons_per_layer,	\
					  layers_names,					\
					  verbose = None):
					  
		self.dataset = dataset
		
		self.iterazioni = iterazioni
		self.learning_rate = learning_rate
		
		self.number_of_inputs = len(dataset[INPUT][0])					# quanti inputs
		self.number_of_layers = len(number_of_neurons_per_layer)		# di quanti strati è composta la rete
		self.number_of_neurons_per_layer = number_of_neurons_per_layer	# numero di neuroni per ciascun layer 
																		# partendo dal layer di output fino a quello di input
		self.layers_names = layers_names								# i nomi/etichette dei vari strati di neuroni
		self.verbose = verbose
		# crea gli strati della rete: parte creando prima lo strato di output
		# e venendo all'indietro attraverso gli strati hidden crea per ultimo
		# lo strato di hidden#1
		self.layers = []
		self.deltas = []
		for i in range(self.number_of_layers-1):
			# se non è il primo strato:
			self.deltas.append([])
			self.layers.append(Neurons(i,									 \
									   self.number_of_neurons_per_layer[i],	 \
									   self.number_of_neurons_per_layer[i+1],\
									   self.layers_names[i],				 \
									   self.learning_rate))
			if self.verbose != None:
				if self.verbose:
					print(f'Created the {self.layers_names[i]} layer made of {self.number_of_neurons_per_layer[i]} neurons and {self.number_of_neurons_per_layer[i+1]} inputs.')
			
		# per il primo strato (hidden#1) :
		self.deltas.append([])
		self.layers.append(Neurons(self.number_of_layers-1,										\
								   self.number_of_neurons_per_layer[self.number_of_layers-1],	\
								   self.number_of_inputs,										\
								   self.layers_names[self.number_of_layers-1],					\
								   self.learning_rate))
		if self.verbose != None:
			if self.verbose:
				print(f'Created the {self.layers_names[self.number_of_layers-1]} layer made of {self.number_of_neurons_per_layer[self.number_of_layers-1]} neurons and {self.number_of_inputs} inputs.')
				
	def get_sigmoid_outputs(self,normalize=None):
		# ritorna gli outputs dello strato di output
		if normalize == None or normalize == False:
			return self.layers[0].get_sigmoid_outputs()
		elif normalize == True:
			output = []
			sigmoid_outputs = self.layers[0].get_sigmoid_outputs()
			try:
				if len(sigmoid_outputs) > 1:
					for sigmoid_output in sigmoid_outputs:
						if sigmoid_output > 0.5:
							output.append(1)
						else:
							output.append(0)
					return tuple(output)
			except TypeError:
				if sigmoid_outputs > 0.5:
					return 1
				else:
					return 0
				
	def get_deltas(self,i):
		# ritorna i delta dello strato i-esimo
		return self.deltas[i]
		
	def save__weights_biases_deltas(self,filename):
		# save the neural network weights, biases & deltas to file.
		weights,biases,deltas = [],[],[]
		
		for layer in reversed(self.layers):
			weights.append(layer.get_weights())
			biases.append(layer.get_biases())
			deltas.append(layer.get_deltas())
			
		with open(filename,"wb") as file:
			pickle.dump(tuple(weights),file)
			pickle.dump(tuple(biases),file)
			pickle.dump(tuple(deltas),file)
			
	def load__weights_biases_deltas(self,filename):
		# load the neural network weights, biases & deltas from file.
		
		with open(filename,"rb") as file:
			weights = pickle.load(file)
			biases = pickle.load(file)
			deltas = pickle.load(file)

		for i,layer in enumerate(reversed(self.layers)):
			layer.set_weights(weights[i])
			layer.set_biases(biases[i])
			layer.set_deltas(deltas[i])
			
	def save(self,filename):
		# save the weights and biases
		self.save__weights_biases_deltas(filename)
		
	def load(self,filename):
		# load the weights and biases
		self.load__weights_biases_deltas(filename)
		
	def reset(self):
		# resetta i neuroni di tutti gli strati della rete
		if self.verbose != None:
			if self.verbose:
				print('\nPerforming RESET.')
		for layer in self.layers:
			layer.reset()
			if self.verbose != None:
				if self.verbose:
					print(f'The {layer.get_name()} layer made of {layer.get_number_of_neurons()} neurons is now initialized.')
			
	def fire(self,inputs=None):
		# calcola il valore di uscita in base a quelli di ingresso ed ai relativi pesi delle connessioni e bias
		# il layer superiore manda i suoi outputs al layer inferiore che li prende come inputs
		next_inputs = inputs
		for layer in reversed(self.layers):
			layer.fire(next_inputs)
			next_inputs = layer.get_outputs()
			
	def calculate_deltas(self,output_atteso):
		# calcola tutti i delta (backpropagation dell'errore)
		for layer in self.layers:
			if layer.get_name() == 'output':
				layer.calculate_deltas_(output_atteso)											# output_effettivo ed output_atteso possono essere una lista di più valori 				
			else:																				# a seconda di quanti neuroni ho. E avrò altrettanti deltas.
				layer.calculate_deltas__(zip(prec_layer.get_deltas(),prec_layer.get_inputs()))	# il delta dei layers successivi dipendono dai delta 
			prec_layer = layer																	# e dai pesi degli inputs, dei layers precedenti.
			layer.calculate_sum_deltas()														# calcola la somma dei delta per lo strato
			
	def backward_update_weights_and_bias(self,output_atteso):
		# backpropagation dell'errore
		self.calculate_deltas(output_atteso)
			
		# dopo aver calcolato il delta di tutti i neuroni della rete si modificano i pesi e i bias di ciascun neurone di ciascun layer.
		for layer in self.layers:
			layer.update_weights_and_bias_by_deltas()
			
	def training_step(self):
		# uno step di training
		choice = random.randint(0,len(self.dataset[0])-1)	# sceglie a caso una coppia (input,output) in base all'indice
		input = self.dataset[INPUT][choice]					# prende un input a caso dal dataset
		output_atteso = self.dataset[OUTPUT][choice]		# prende il relativo output atteso
		# print(f'Dataset: {choice}')
		# print(f'Inputs: {input}')
		# print(f'output atteso: {output_atteso}')
		
		self.fire(input)
		
		self.backward_update_weights_and_bias(output_atteso)
		
	def training(self,verbose=False):
		# addestramento della rete neurale
		
		# self.reset()
		t = time.time()
		for iterazione in range(1,self.iterazioni+1):
			if iterazione % int(self.iterazioni/10) == 0:
				dt = time.time() - t
				if verbose: print(f'ITERAZIONE {iterazione} - dT = {int(dt)} sec. - {int(10*dt/60)/10} min. - {int((self.iterazioni/10)/dt)} iterazioni/sec.')
				t = time.time()
				
			self.training_step()	# un passo di addestramento
			
			for i in range(self.number_of_layers):
				self.deltas[i].append(self.layers[i].get_sum_deltas()) # memorizza i delta di ogni strato
				
	def test(self,verbose=False):
		risultato_corretto = 0
		# for data in self.dataset:
		for i,input in enumerate(self.dataset[INPUT]):
			if verbose: print(f'Input di test: {input}')
			outputs_attesi = self.dataset[OUTPUT][i]	# ne prende gli outputs
			if verbose: print(f'Outputs attesi: {str(outputs_attesi)}')
			self.fire(input)
			outputs_effettivi = self.get_sigmoid_outputs()
			if verbose: print(f'Outputs effettivi: {str(outputs_effettivi)}')
			
			if len(outputs_attesi) > 1:
				for output_effettivo,output_atteso in zip(outputs_effettivi,outputs_attesi):
					if output_effettivo > 0.5:
						if output_atteso == 1:
							if verbose: print(input,output_atteso,'--> 1')
							risultato_corretto += 1
						else:
							if verbose: print(input,output_atteso,'--> 1 (!output effettivo errato!)')
					elif output_effettivo <= 0.5:
						if output_atteso == 0:
							if verbose: print(input)
							risultato_corretto += 1
						else:
							if verbose: print(input,output_atteso,'--> 0 (!output effettivo errato!)')
			else:
				# nel caso di una sola uscita (un solo neurone di uscita)
				output_effettivo = outputs_effettivi
				output_atteso = outputs_attesi[0]
				if output_effettivo > 0.5:
					if output_atteso == 1:
						if verbose: print(input,output_atteso,'--> 1')
						risultato_corretto += 1
					else:
						if verbose: print(input,output_atteso,'--> 1 (!output effettivo errato!)')
				elif output_effettivo <= 0.5:
					if output_atteso == 0:
						if verbose: print(input,output_atteso,'--> 0')
						risultato_corretto += 1
					else:
						if verbose: print(input,output_atteso,'--> 0 (!output effettivo errato!)')
			
		self.affidabilita = 100*risultato_corretto/(len(outputs_attesi)*len(self.dataset[0]))
		
		if verbose:
			print(f'Risultato corretto:{risultato_corretto/len(outputs_attesi)}')
			print(f'Len(dataset)={len(self.dataset[INPUT])}')
			print(f'\noutput_effettivo affidabile nel {self.affidabilita} % dei casi\n')
		
		return self.affidabilita
	

# neurons.py : implementazione di uno strato di neuroni in Python
#
# CopyRight 2021 by Lumachina Software - @_°° 
# Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

from neuron import Neuron

INPUT,OUTPUT = 0,1

class Neurons():
	
	def __init__(self,index,				\
					  number_of_neurons,	\
					  number_of_inputs,		\
					  name = None,			\
					  learning_rate = None,	\
					  dataset = None,		\
					  iterazioni = None):

		self.index = index
		
		self.neurons = []		# lista dei neuroni che compongono lo strato
		
		self.number_of_neurons = number_of_neurons	# numero di neuroni che compongono lo strato
		self.number_of_inputs = number_of_inputs	# numero di inputs per neurone
		
		self.sum_deltas = 0
		
		if name != None:
			self.name = name	# nome dello strato di neuroni
		else:
			self.name = 'Layer 0'
		
		if iterazioni != None:
			self.iterazioni = iterazioni
		
		if learning_rate != None:
			self.learning_rate = learning_rate
			
		if dataset != None:
			self.dataset = dataset	
			for i in range(self.number_of_neurons):
				self.neurons.append(Neuron(self.number_of_inputs,self.learning_rate,(self.dataset[INPUT][i],self.dataset[OUTPUT][i]),self.iterazioni))
				self.neurons[i].index = i	# ogni neurone dello strato viene numerato
		else:		
			for i in range(self.number_of_neurons):
				self.neurons.append(Neuron(self.number_of_inputs,self.learning_rate))
				self.neurons[i].index = i	# ogni neurone dello strato viene numerato
			
	def get_neuron(self,i):
		# ritorna il neurone i-esimo
		return self.neurons[i]
		
	def get_number_of_neurons(self):
		# ritorna il numero di neuroni del layer
		return self.number_of_neurons
		
	def get_name(self):
		# ritorna il nome del layer
		return self.name
		
	def get_inputs(self):
		# ritorna una tupla con gli inputs di ciascun neurone
		inputs = []
		for neuron in self.neurons:
			inputs.append(neuron.get_inputs())
		return tuple(inputs)
		
	def get_outputs(self):
		# ritorna una tupla con gli outputs di ciascun neurone
		outputs = []
		for neuron in self.neurons:
			outputs.append(neuron.get_output())
		if len(self.neurons) == 1:
			return outputs[0]
		else:
			return tuple(outputs)
			
	def get_deltas(self):
		# ritorna una tupla con i delta di ciascun neurone
		# ripetuti tante volte quanti sono gli ingressi del neurone
		deltas = []
		for neuron in self.neurons:
			deltas.append(tuple([neuron.get_delta()]*neuron.get_number_of_inputs()))
		return tuple(deltas)
		
	def get_sigmoid_outputs(self):
		outputs = []
		for neuron in self.neurons:
			outputs.append(neuron.get_sigmoid_output())
		if len(self.neurons) == 1:
			return outputs[0]
		else:
			return tuple(outputs)
		
	def get_weights(self):
		weights = []
		for neuron in self.neurons:
			weights.append(neuron.get_weights())
		return tuple(weights)
		
	def get_biases(self):
		biases = []
		for neuron in self.neurons:
			biases.append(neuron.get_bias())
		return tuple(biases)
		
	def get_sum_deltas(self):
		# ritorna la somma dei delta per lo strato
		return self.sum_deltas
		
	def set_weights(self,weights):
		for i,neuron in enumerate(self.neurons):
			neuron.set_weights(weights[i])
			
	def set_biases(self,biases):
		for i,neuron in enumerate(self.neurons):
			neuron.set_bias(biases[i])
	
	def set_deltas(self,deltas):
		for i,neuron in enumerate(self.neurons):
			neuron.set_delta(deltas[i])
			
	def reset(self):
		# resetta i neuroni
		for neuron in self.neurons:
			neuron.reset()
			
	def fire(self, inputs = None):
		# calcola il valore di uscita in base a quelli di ingresso e ai relativi pesi delle connessioni
		for neuron in self.neurons:
			neuron.fire(inputs)
		
	def training(self):
		# addestramento: calcola i pesi e il bias dei neuroni
		for neuron in self.neurons:
			neuron.training()
	
	def calculate_sum_deltas(self):
		# ritorna la somma dei delta dello strato
		self.sum_deltas = 0
		for neuron in self.neurons:
			self.sum_deltas += neuron.get_delta()
		
	def calculate_deltas_(self,outputs_attesi):
		# calcola il delta dell'errore per lo strato di output
		for i,neuron in enumerate(self.neurons):
			output_effettivo = neuron.get_sigmoid_output()
			err = outputs_attesi[i] - output_effettivo
			neuron.set_delta(err*output_effettivo*(1-output_effettivo))
	
	def calculate_deltas__(self,preceding_layer_delta_and_inputs):
		# calcola il delta dell'errore per gli altri strati
		for neuron in self.neurons:
			err = 0
			for j,(delta,input) in enumerate(preceding_layer_delta_and_inputs):
				err += delta[j]*input[j]
			output_effettivo = neuron.get_sigmoid_output()
			neuron.set_delta(err*output_effettivo*(1-output_effettivo))
		
	def update_weights_and_bias_by_deltas(self):
		# aggiorna i pesi e i bias del layer in base ai delta dei neuroni del layer.
		for neuron in self.neurons:
			neuron.update_weight_and_bias_by_delta()
		
	def test(self,verbose=False):
		# testa il dataset stampando i risultati
		for neuron in self.neurons:
			neuron.test(verbose)

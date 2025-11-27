
# Generate string for Kolmogorov complexity calculation purposes

import string
import random

def generate_constant_string(message,size):
	return message*size
	
def generate_random_string(size):
	message = ''
	for i in range(size):
		message += random.choice(string.ascii_letters)
		
	return message
	
def main():

	size = 1000000
	# print(generate_constant_string('ab',size))
	print(generate_random_string(size))
	
main()
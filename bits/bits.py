
#bits.py : libreria sulla manipolazione dei bits

# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
def testBit(int_type, offset):
	return int_type & (1 << offset)

# setBit() returns an integer with the bit at 'offset' set to 1.
def setBit(int_type, offset):
	return int_type | (1 << offset) # setta a 1 il bit n-esimo del byte R (8-bit)

# clearBit() returns an integer with the bit at 'offset' cleared.
def clearBit(int_type, offset):
	return int_type & ~(1 << offset) # setta a 0 il bit n-esimo del byte R (8-bit)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
def toggleBit(int_type, offset):
	return int_type ^ (1 << offset)
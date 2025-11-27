' LZW compression/decompression algorithm
const MAX_DICT = 4096			'max dictionary dimension
dim shared as integer N_DICT	'dictionary dimension

public function dict_contains(dict() as string, wc as string) as boolean
	for i as integer = 0 to ubound(dict)
		if dict(i) = wc then
			return TRUE
		end if
	next i
	return FALSE
end function
public function dict_contains_(dict() as string, i as integer) as boolean
	if i <= ubound(dict) then
		if dict(i) <> "" then return TRUE
	end if
	return FALSE
end function
public function find_dict(dict() as string, w as string) as integer
	for i as integer = 0 to ubound(dict)
		if dict(i) = w then
			return i
		end if
	next i
	return 0
end function
public sub		print_dictionary(dict() as string)
	dim as integer n
	print:print "dictionary: "
	for i as integer = 256 to ubound(dict)
		if dict(i) <> "" then
			print dict(i);", ";
		else
			n = i
			exit for
		end if
	next i
	print:print "dictionary contains";n-256;" elements."
	N_DICT = n-256
end sub
public function make_dict(dict() as string, s as string) as integer
	'make initial dictionary
	for i as integer = 0 to 255
		dict(i) = chr$(i)
	next i
	return 256
	'for i as integer = 0 to len(s)-1
	'	dict(i) = mid$(s,i,1)
	'next i
	'return len(s)
end function
public function compress(compressed() as integer, uncompressed as string) as boolean
	'build the dictionary
	dim as string dict(MAX_DICT)
	dim as integer nd = make_dict(dict(),uncompressed)
	'compressing
	dim as string wc, w = ""
	dim as integer j
	dim as integer nc = 0
	if len(uncompressed) > 0 then
		for i as integer = 1 to len(uncompressed)
			wc = w + mid$(uncompressed,i,1) ': print wc
			if dict_contains(dict(),wc) then
				w = wc
			else
				'write w to output
				compressed(nc) = find_dict(dict(),w)
				nc = nc + 1
				'wc is a new sequence; add it to the dictionary
				dict(nd) = wc
				nd = nd + 1
				w = mid$(uncompressed,i,1)
			end if
		next i
		'write remaining output if necessary
		if w <> "" then
			compressed(nc) = find_dict(dict(),w)
			nc = nc + 1
		end if
		print_dictionary(dict())
		return TRUE
	else
		print"error: cannot compress a zero lenght object"
		return FALSE
	end if
end function
public function decompress(compressed() as integer) as string
	'build the dictionary
	dim as string dict(MAX_DICT)
	dim as integer nd = make_dict(dict(),"")
	dim as integer k,n = 0
	'decompressing
	dim as string w = dict(compressed(0))
	dim as string entry
	dim as string decompressed = w
	for i as integer = 1 to ubound(compressed) 'salta il primo
		if compressed(i) <> 0 then
			k = compressed(i)
			entry = ""
			if dict_contains_(dict(),k) then
				entry = dict(k)
			elseif k = nd then
				entry = w + left$(w,1)
			end if
			decompressed = decompressed + entry
			'new sequence; add it to the dictionary
			dict(nd) = w + left$(entry,1)
			nd = nd + 1
			w = entry
		else
			exit for
		end if
	next i
	print_dictionary(dict())
	return decompressed
end function
public sub		initialize(v() as integer)
	for i as integer = 0 to ubound(v)
		v(i) = 0
	next i
end sub
public sub		print_compressed(compressed() as integer)
	dim as integer n
	print:print "compressed: "
	for i as integer = 0 to ubound(compressed)
		if compressed(i) <> 0 then
			print compressed(i);", ";
		else
			n = i
			exit for
		end if
	next i
	print:print "compressed object contains";n;" elements."
end sub

' --- main

dim as integer compressed(0 to 10000) : initialize(compressed())
dim as string decompressed = space(10000)

dim as string s
input "give the string to be compressed: ";s
print "string length:";len(s)

if compress(compressed(),s) then
	print_compressed(compressed())
	decompressed = decompress(compressed())
	print:print "decompressed: " : print decompressed
	print "decompressed object contains";len(decompressed);" elements."
	print "compression ratio:";1-N_DICT/len(decompressed)
end if

end 0

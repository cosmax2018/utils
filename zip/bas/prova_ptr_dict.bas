'questo programma serve per dimostrare
'come va utilizzato il puntatore al dizionario

public function compress(w as string) as byte ptr '<---veramente e' meglio usare ushort che e' a 16-bits
	dim as byte ptr pDict = allocate(len(w)*sizeof(byte))
	for i as integer = 0 to len(w)-1
		pDict[i] = asc(mid$(w,i+1,1))
	next i
	pDict[len(w)] = 0
	return pDict
end function
public function decompress(pDict as byte ptr) as string
	dim as string w = ""
	dim as integer i = 0
	while pDict[i] > 0
		w = w + chr$(pDict[i])
		i = i + 1
	wend
	return w
end function

' --- main
dim as string z
input "give me a string (max 255 char) :";z
print "A:compressing.."
dim as byte ptr pDictionary = compress(z)
print "B:printing dictionary.."
dim as integer i = 0
while pDictionary[i] > 0
	print chr$(pDictionary[i])
	i = i + 1
wend
print "C:decompressing.."
dim as string s = decompress(pDictionary)
print "D:printing decompressed string.."
print s
print "End"
end 0

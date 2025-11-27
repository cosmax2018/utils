'implementazione dell'algoritmo di compressione/decompressione LZW

#include "file.bi"

dim as string input_filename = CurDir & "\test.txt"
dim as string output_filename = CurDir & "\zipped.txt"
dim as string decoded_filename = CurDir & "\unzipped.txt"
dim as string dictionary(255)

declare sub			set_up_dictionary(as string, d() as string)
declare function	dictionary_contains(as string, d() as string) as boolean
declare function	dictionary_find(as string, d() as string) as byte
declare sub			add_to_dictionary(as string, d() as string)
declare function	get_dictionary(d() as string) as integer
declare sub			encode_to_file(as string, d() as string, as integer)
declare sub			compress(as string, as string, d() as string)
declare sub			decompress(as string, as string, d() as string)

' --- main

compress(input_filename, output_filename, dictionary())

decompress(output_filename, decoded_filename, dictionary())

end 0

' --- procedures & functions

sub			compress(i_filename as string, o_filename as string, dict() as string)
	dim as ubyte c
	dim as string s = ""
	dim as string*1 ch
	set_up_dictionary(i_filename, dict())

	open i_filename for input as #1
	open o_filename for output as #2

	while not eof(1)
		get #1,,c : ch = chr$(c) 'read a character
		if dictionary_contains(s+ch, dict()) then
			s = s+ch
		else
			encode_to_file(s,dict(),2)
			add_to_dictionary(s+ch, dict())
			s = ch
		end if
	wend

	encode_to_file(s,dict(),2)

	close #2
	close #1


	dim as integer n = get_dictionary(dict())

	print "ci sono ";n;" simboli nel dizionario"
	print " la lunghezza in caratteri del file da comprimere e' ";FileLen(i_filename)
	print " la lunghezza in caratteri del file compresso e' ";FileLen(o_filename)
	print "indice di compressione :";FileLen(o_filename)/FileLen(i_filename)
	print "indice di complessita' :";n/FileLen(i_filename)
end sub
sub			decompress(i_filename as string, o_filename as string, dict() as string)
	'decompress

end sub
sub			set_up_dictionary(filename as string, dict() as string)
	dim as integer n = 1
	dim as ubyte c
	dim as string*1 ch
	open filename for input as #1
		while not eof(1)
			get #1,,c : ch = chr$(c) 'read a character
			if not dictionary_contains(ch, dict()) then
				dict(n) = ch
				n = n + 1
			end if
		wend
	close #1
	print "the dictionary has ";n;" initial elements."
end sub
function	dictionary_contains(w as string, dict() as string) as boolean
	for i as integer = 1 to 255
		if dict(i) = w then return true
	next i
	return false
end function
function	dictionary_find(w as string, dict() as string) as byte
	for i as integer = 1 to 255
		if dict(i) = w then return i
	next i
	return 0
end function
sub			add_to_dictionary(w as string, dict() as string)
	dim as integer i = 1
	while not dict(i) = ""
		i = i + 1
	wend
	dict(i) = w
end sub
function	get_dictionary(dict() as string) as integer
	'print the dictionary
	dim as integer n = 0
	for i as integer = 1 to 255 
		if dict(i) <> "" then 
			print dict(i) 
			n = n + 1
		end if
	next i
	return n
end function
sub			encode_to_file(w as string, dict() as string, f as integer)
	dim as byte n = dictionary_find(w,dict())
	if n <> 0 then
		put #f,,n
	end if
end sub

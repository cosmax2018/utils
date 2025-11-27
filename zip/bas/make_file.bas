' questo programma genera un file casuale di caratteri
' che poi puo' essere compresso con LZW

#include "file.bi"

const _TERMINATORE_ = ""
dim shared as string _ALPHABET_ : _ALPHABET_ = "ABCDEFGHIJKLMNOPQRSTUVWZXabcdefghijklmnopqrstuvwzx 1234567890" 'default alphabet

public function make_file(n as integer, f as integer) as boolean
	'make the random file
	dim as string*1 ch
	for i as integer = 1 to n
		ch = mid$(_ALPHABET_,1+rnd()*(len(_ALPHABET_)-1),1)
		print #f,ch;
	next i
	print #f, _TERMINATORE_
	return true
end function


' --- main

'es. make_file test.txt 1000             genera un file da comprimere di nome test.txt lungo 1000 bytes
'es. make_file test_ab.txt 1000 ABCD     genera un file basato sull'alfabeto ABCD

dim as string output_filename = CurDir & "\" & command$(1)	' file da scrivere in output
dim as integer n = cint(command$(2))						' file length
if command$(3) <> "" then _ALPHABET_ = command$(3)			' alfabeto passato come parametro

randomize timer

if output_filename <> "" then
	open output_filename for output as #2
		if make_file(n,2) then
			print "random file generated."
		else
			print "error generating random file!"
		end if
	close #2
else
	print "parameter error: file name empty."
	end 0
end if
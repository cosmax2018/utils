' questo programma genera un file compresso casuale di caratteri
' che poi puo' essere decompresso con LZW
'
' il file e' compresso nel senso che e' sperabilmente decomprimibile con LZW
' questo programma serve a testare la decomprimibilita' di files casuali

#include "file.bi"

public sub		write_file(outfile as string, buffer() as ushort)
	' writes 16-bits values into outfile
	if FileExists(outfile) then kill(outfile)
	open outfile for binary as #2
		for i as integer = 1 to UBound(buffer)
			if buffer(i) <> 0 then
				put #2,,buffer(i)
			else
				exit for
			end if
		next i
	close #2
end sub
public function make_zipfile(n as integer, outfile as string) as boolean
	'make the random file of 16-bits values
	dim as ushort buffer(n)
	for i as integer = 1 to n
		buffer(i) = 1 + cushort(rnd()*65535)
	next i
	write_file(outfile,buffer())
	return true
end function


' --- main

'es. make_zipfile test.zip 1000             genera un file da decomprimere di nome test.zip lungo 1000 bytes

dim as string output_filename = CurDir & "\" & command$(1)	' file da scrivere in output
dim as integer n = cint(command$(2))						' file length

randomize timer

if output_filename <> "" then
	' per ogni numero a 16-bits occorrono 2 bytes da 8-bit per cui occorre dividere n per 2
	if make_zipfile(n\2,output_filename) then
		print "random file generated."
	else
		print "error generating random file!"
	end if
else
	print "parameter error: file name empty."
	end 0
end if

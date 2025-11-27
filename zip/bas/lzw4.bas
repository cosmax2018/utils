'
' LZW compression/decompression algorithm written in FreeBasic
' 
' CopyRight 2018 by Lumachina Software @_°°
' Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)

#include "file.bi"

dim shared as integer MAX_DICT = 65535		' max dictionary dimension is 64kb
dim shared as integer MAX_BUFFER = 1048560	' max zipped file dimension is 1Mb

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
public function find_dict(dict() as string, w as string) as ushort
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
end sub
public function make_dict(dict() as string, infile as string) as integer
	'make initial dictionary
	for i as integer = 0 to 255
		dict(i) = chr$(i)
	next i
	return 256
end function
public sub		read_file(infile as string, buffer() as ushort)
	' reads 16-bits values from infile
	dim as integer i = 0
	open infile for binary as #1
		while not eof(1)
			i = i + 1
			get #1,,buffer(i)
		wend
	close #1
end sub
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
public function compress(infile as string, outfile as string) as boolean
	'build the dictionary
	dim as string dict(MAX_DICT)
	dim as integer nd = make_dict(dict(),infile)
	dim as ushort buffer(MAX_BUFFER) 'contains 16-bit from 0 to 65535 values
	'compressing
	dim as string wc, w = ""
	dim as string*1 ch
	dim as integer i = 0
	dim as integer nc = 0
	if filelen(infile) > 0 then
		open infile for input as #1
		while not eof(1)
			get #1,,ch
			wc = w + ch
			if dict_contains(dict(),wc) then
				w = wc
			else
				'write w to output buffer
				i = i + 1
				buffer(i) = find_dict(dict(),w)
				'wc is a new sequence; add it to the dictionary
				dict(nd) = wc
				nd = nd + 1
				w = ch
			end if
		wend
		'write remaining output if necessary
		if w <> "" then
			i = i + 1
			buffer(i) = find_dict(dict(),w)
		end if
		print_dictionary(dict())
		close #1
		' write to output file
		write_file(outfile,buffer())
		return TRUE
	else
		print"error: cannot compress a zero lenght object"
		return FALSE
	end if
end function
public function decompress(infile as string, outfile as string) as boolean
	'build the dictionary
	dim as string dict(MAX_DICT)
	dim as integer nd = make_dict(dict(),"")
	dim as ushort buffer(MAX_BUFFER) 'contains 16-bit from 0 to 65535 values
	dim as integer k
	'decompressing
	dim as string w
	dim as string entry
	dim as integer m
	'read from infile
	read_file(infile,buffer())
	w = dict(buffer(1))
	open outfile for output as #2
	print #2, w;
	for i as integer = 2 to UBound(buffer) 
		m = buffer(i)
		if m <> 0 then
			k = m
			entry = ""
			if dict_contains_(dict(),k) then
				entry = dict(k)
			elseif k = nd then
				entry = w + left$(w,1)
			end if
			print #2,entry;
			'new sequence; add it to the dictionary
			dict(nd) = w + left$(entry,1)
			nd = nd + 1
			w = entry
		else
			exit for
		end if
	next i
	close #2
	print_dictionary(dict())
	return TRUE
end function

' --- main

dim as string mode = command$(1)							' -zip   or  -unzip
dim as string input_filename = CurDir & "\" & command$(2)	' filename to zip or to unzip
dim as string zipped_filename
dim as string unzipped_filename

if instr(UCase(mode),"-ZIP") > 0 then
	if input_filename <> "" then
		if FileExists(input_filename) then
			zipped_filename = left$(input_filename,len(input_filename)-4) & ".zip"
			if compress(input_filename,zipped_filename) then
				print "original file is";filelen(input_filename);" bytes lenght."	
				print "compressed file is";filelen(zipped_filename);" bytes lenght."
				print "compression ratio:";100-100*filelen(zipped_filename)/filelen(input_filename);"%"
			else
				print "something went wrong...compression error!"
			end if
		else
			print "file does not exists, have to pass the correct name of the file to be zipped."
			print
			print "example:  lzw4 -zip test.txt"
			print
			end 0			
		end if
	else
		print "parameter 2 error! file name empty."
		end 0
	end if
	
elseif instr(Ucase(mode),"-UNZIP") > 0 then
	if input_filename <> "" then
		if FileExists(input_filename) then
			unzipped_filename = left$(input_filename,len(input_filename)-4) & ".unzip"
			if decompress(input_filename,unzipped_filename) then
				print "compressed file is";filelen(zipped_filename);" bytes lenght."	
				print "decompressed file is";filelen(unzipped_filename);" bytes lenght."
				print "decompression ratio:";100-100*filelen(zipped_filename)/filelen(unzipped_filename);"%"				
			else
				print "something went wrong...decompression error!"
			end if
		else
			print "file does not exists, have to pass the correct name of the file to be unzipped."
			print
			print "example:  lzw4 -unzip test.zip"
			print
			end 0			
		end if		
	else
		print "parameter 2 error! file name empty."
		end 0
	end if

else
	print "parameter 1 error! mode of operation uncorrect"
	print
	print "examples:  lzw4 -zip test.txt"
	print "           lzw4 -unzip test.zip"	
	print	
end if

end 0

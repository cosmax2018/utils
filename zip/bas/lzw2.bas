' LZW compression/decompression algorithm

#include "file.bi"

dim shared as integer MAX_DICT = 65535	' max dictionary dimension is 64k
dim shared as integer N_DICT			' dictionary dimension

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
public function find_dict(dict() as string, w as string) as string
	for i as integer = 0 to ubound(dict)
		if dict(i) = w then
			return str$(i)	'converto in stringa perche' tenga meno spazio
		end if
	next i
	return ""
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
public function make_dict(dict() as string, infile as string) as integer
	'make initial dictionary
	for i as integer = 0 to 255
		dict(i) = chr$(i)
	next i
	return 256
end function
public function compress(infile as string, outfile as string) as boolean
	'build the dictionary
	dim as string dict(MAX_DICT)
	dim as integer nd = make_dict(dict(),infile)
	'compressing
	dim as string wc, w = ""
	dim as string*1 ch
	dim as integer j
	dim as integer nc = 0
	if filelen(infile) > 0 then
		open infile for input as #1
		open outfile for output as #2
		while not eof(1)
			get #1,,ch
			wc = w + ch
			if dict_contains(dict(),wc) then
				w = wc
			else
				'write w to output
				print #2, find_dict(dict(),w);",";
				'wc is a new sequence; add it to the dictionary
				dict(nd) = wc
				nd = nd + 1
				w = ch
			end if
		wend
		'write remaining output if necessary
		if w <> "" then
			print #2, find_dict(dict(),w)
		end if
		print_dictionary(dict())
		close #2
		close #1
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
	dim as integer k,n = 0
	'decompressing
	dim as string w
	dim as string entry
	dim as integer m
	open infile for input as #1
	input #1, m : w = dict(m)
	open outfile for output as #2
	print #2, w;
	while not eof(1)
		input #1, m
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
			exit while
		end if
	wend
	close #2
	close #1
	print_dictionary(dict())
	return TRUE
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

dim as string input_filename = CurDir & "\" & command$(1)								 '"\test.txt"
dim as string zipped_filename
dim as string unzipped_filename

if input_filename <> "" then
	if fileexists(input_filename) then
		zipped_filename = left$(input_filename,len(input_filename)-4) & ".zip"		 'CurDir & "\zipped.txt"
		unzipped_filename = left$(input_filename,len(input_filename)-4) & ".unzip"	 'CurDir & "\unzipped.txt"
	else
		print "file does not exists, have to pass the correct name of the file to be compressed."
		print
		print "example:  lzw_2 test.txt"
		print
		end 0
	end if
else
	print "parameter error: file name empty."
	end 0
end if

if compress(input_filename, zipped_filename) then
	print "compressed file is";filelen(zipped_filename);" bytes lenght."
	'
	if decompress(zipped_filename, unzipped_filename) then
		print "compressed file is";filelen(zipped_filename);" bytes lenght."	
		print "decompressed file is";filelen(unzipped_filename);" bytes lenght."
		print "compression ratio:";100-100*filelen(zipped_filename)/filelen(unzipped_filename);"%"
	else
		print "decompression error!"
	end if
else
	print "compression error!"
end if

end 0

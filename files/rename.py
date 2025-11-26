
# rename.py: batch renaming files 

import os

def change_working_directory():
	while True:
		directory = input('Directory:')
		if os.path.isdir(directory):
			os.chdir(directory)
			print(os.getcwd())
			break
		else:
			print('The directory given does not exists!')
	
def main():
	
	change_working_directory()
	
	prefix ='3'
	# suffix = '_suffix'
	
	# prefix = input("Prefix: ")
	# suffix = input("Suffix: ")
	
	for f in os.listdir():
		f_name, f_ext = os.path.splitext(f)
		
		old_file = '{}{}{}'.format(f_name,f_ext,suffix)
		
		new_file = '{}{}{}'.format(prefix,f_name,f_ext)
		
		# new_file = '{}{}'.format(f_name[9:],f_ext) # per ripristinare !
		
		os.rename(f, new_file)
		
		print('{} --> {}'.format(old_file,new_file))
main()


# collatz.py : soluzione alla congettura di Collatz

def step(a):
	# un passo..
	if a%2 == 0:
		return a//2
	else:
		return 3*a+1
		
def run(a):
    # esegue tutto il ciclo che porta alla convergenza, ovvero a 1
    i=1
    while a!=1:
        a=step(a)
        print(f"{i}:{a}")
        i+=1
        
def main():
    while 1:
        a=int(input("\nInserisci il numero di partenza (0 per terminare) : "))
        if a==0:
            break
        else:
            run(a)
main()
 
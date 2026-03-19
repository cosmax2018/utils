
# collatz_iter_v2.py : soluzione alla congettura di Collatz

def step(a):
	# un passo..
	if a%2 == 0:
		return a//2
	else:
		return 3*a+1
		
def run(a):
    # esegue tutto il ciclo che porta alla convergenza, ovvero a 1
    # e ritorna il numero di passi necessari alla convergenza.
    i=1
    while a!=1:
        a=step(a)
        # print(f"{i}:{a}")
        if a==1:
            return i   # evita di incrementare di i quando non serve
        i+=1
        
def main():
    for a in range(1,1_000_000_000_000_000):
        print(a)
        while a!=1:
            a=run(a)
main()
 

# collatz_iter_v3.py : soluzione alla congettura di Collatz

def step(a):
    if a % 2 == 0:
        return a // 2
    else:
        return 3 * a + 1


def collatz_steps(n):
    """Restituisce il numero di passi per arrivare a 1"""
    count = 0
    while n != 1:
        n = step(n)
        count += 1
    return count


def iterate_f(n, max_iter=50):
    """Applica f iterativamente e rileva cicli"""
    seen = {}
    sequence = []

    for i in range(max_iter):
        if n in seen:
            # ciclo trovato
            start = seen[n]
            cycle = sequence[start:]
            return sequence, cycle

        seen[n] = i
        sequence.append(n)

        n = collatz_steps(n)

    return sequence, None


def main():
    limite = 50  # puoi aumentarlo

    for n in range(1, limite + 1):
        seq, cycle = iterate_f(n)

        if cycle:
            if len(cycle) == 1:
                print(f"{n}: punto fisso -> {cycle[0]}")
            else:
                print(f"{n}: ciclo -> {cycle}")
        else:
            print(f"{n}: nessun ciclo trovato (limite iterazioni)")


main()
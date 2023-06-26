def gcd(a : int, b : int) -> int:
    while b != 0: # follows directly from the euclidean alg.
        temp = a
        a = b
        b = temp % b
    return a


def coprime(a : int, b : int) -> int: # follows from the definition of coprimes
    return gcd(a, b) == 1



# for integer n > 0

def totient (n : int) -> int:
    if n == 1: 
        return 1

    count : int = 1
    for i in range(2,n):
        if (gcd(i, n) == 1):
            count += 1

    return count



def theorem_func ( a : int, n : int , verbose : bool = False) -> bool:
    if (verbose):
        print(f"totient: {totient(n)}, a ** totient: {a ** totient(n)}") # should probably just record these in variables for efficiency

    return( ( (  ( a ** totient(n) ) - 1 ) % n ) == 0 )
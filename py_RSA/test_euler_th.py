from typing import List
import eulers_theorem as eu_th

# adjust the flags to run different tests:
checkTotient : bool = False
checkTheorem : bool = False
checkTheorem_onlyPrimes : bool = False

primes : List[int] = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]

if checkTotient:
    for i in range(len(primes)):
        print(primes[i],eu_th.totient(primes[i]), sep = "\t")


if checkTheorem: # "I don't believe in anything I cannot see myself" -- Abraham J. MyNameIsMadeupson
    evenNum : int = 20
    stop : int
    if (checkTheorem_onlyPrimes): 
        stop = int(len(primes)/2)
    else:
        stop : int = len(primes)

    for i in range(1, int(stop) ):
        print(primes[i], (primes[len(primes) - i]) if  (checkTheorem_onlyPrimes) else (evenNum), eu_th.theorem_func(primes[i], (primes[len(primes) - i]) if  (checkTheorem_onlyPrimes)  else (evenNum), verbose = True))



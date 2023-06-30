import eulers_theorem as euth
import rsa as rsa
from typing import Tuple
from typing import List

# modular exponentiation test function
def modExpoTest(a : int = 2) -> None:
    m : int
    n : int
    
    primes : List[int] = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
    print('\n')

    for i in range( len(primes) ):
        m = i
        n = primes[i]
        test : int = rsa.modExponent(a, m, n)
        print( f"Found: {a} ^ {m} % {n} = {test}" , ( ("PASSED") if ( test == ( (a ** m) % n )) else ("FAIL") ), sep='\t\t')



def rsa_test_base(p, q, verbose) -> Tuple[int, int, int]:
    if (p * q <= 256):
        raise Exception(f"Not all ascii characters could be encrypted and decrypted with p = {p} and q = {q}. Please pick p and q such that p * q > 256")

    n : int = p * q
    totn : int = euth.totient(n)

    if (verbose):
        print(f"p := {p}, q := {q}, n := {n}")
        print(f"totient(n) = {totn}")

    d : int = rsa.findSuitableD(p, q)
    e : int = rsa.modInverse(d, totn)

    if (verbose):
        print(f"d = {d}, e = {e}, (e * d) mod tot(n) = { ( e * d) % totn }")
    
    return n,d,e



def rsa_singleCharTest(Message : str, p : int , q : int, verbose : bool = False ) -> None:
    n : int
    d : int
    e : int
    n, d, e = rsa_test_base(p, q, verbose)

    M : int = ord(Message)
    C: int = rsa.enc_dec_singleChar(M, e, n)
    decResult : int = rsa.enc_dec_singleChar(C, d, n)

    print(f"Message: {M}, Ciphertext: {C}, decrypted result: {decResult}")




def rsa_wordTest(M: str, p : int, q : int, verbose: bool = False) -> None:
    n : int
    d : int
    e : int
    n, d, e = rsa_test_base(p, q, verbose)

    C: str = rsa.rsa_word(M, e, n)
    decResult : str = rsa.rsa_word(C, d, n)

    print(f"Message: {M}, Ciphertext: {C}, decrypted result: {decResult}")




# test main:

rsa_wordTest("insert creative test message here", 13, 23)

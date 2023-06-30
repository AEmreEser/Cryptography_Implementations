import euler_theorem as euth
import test_totient as testTot
import rsa as rsa


# modular exponentiation test function
def modExpoTest(a : int = 2) -> None:
    m : int
    n : int
    
    print('\n')

    for i in range( len(testTot.primes) ):
        m = i
        n = testTot.primes[i]
        test : int = rsa.modExponent(a, m, n)
        print( f"Found: {a} ^ {m} % {n} = {test}" , ( ("PASSED") if ( test == ( (a ** m) % n )) else ("FAIL") ), sep='\t\t')


def rsa_singleCharTest(Message : str, p : int , q : int ) -> None:

    if (p * q <= 256):
        raise Exception(f"Not all ascii characters could be encrypted and decrypted with p = {p} and q = {q}. Please pick p and q such that p * q > 256")

    n : int = p * q
    totn : int = euth.totient(n)

    print(f"p := {p}, q := {q}, n := {n}")
    print(f"totient(n) = {totn}")

    d : int = rsa.findSuitableD(p, q)
    e : int = rsa.modInverse(d, totn)

    print(f"d = {d}, e = {e}, (e * d) mod tot(n) = { ( e * d) % totn }")

    M : int = ord(Message)
    C: int = rsa.enc_dec_singleChar(M, e, n)
    decResult : int = rsa.enc_dec_singleChar(C, d, n)

    print(f"Message: {M}, Ciphertext: {C}, decrypted result: {decResult}")


def rsa_word_test(M: str, p : int, q : int, verbose: bool = False) -> None:

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

    C: str = rsa.rsa_word(M, e, n)
    decResult : str = rsa.rsa_word(C, d, n)

    print(f"Message: {M}, Ciphertext: {C}, decrypted result: {decResult}")


# test main:

# modExpoTest(5)
# modExpoTest(2)

# rsa_singleCharTest('T', 29, 31)

rsa_word_test("test test pesp pesp", 29, 31)

rsa_word_test("insert creative test message here", 13, 23)

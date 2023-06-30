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



# test main:

# modExpoTest(5)
# modExpoTest(2)

p : int = testTot.primes[7]
q : int = testTot.primes[10]
n : int = p * q

print(f"p := {p}, q := {q}, n := {n}")
print(f"totient(n) = {euth.totient(n)}")



M : int = ord('C')
C: int = rsa.enc_dec_singleChar(M, e_d=13, n=n)
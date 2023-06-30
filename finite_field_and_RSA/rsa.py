import euler_theorem as eu_th
from typing import List




# calculates: a^m mod n
def modExponent(a : int, m : int, n: int) -> int: # algorithm due Diadel
    if (a <= 0 or m < 0 or n <= 1):
        raise ValueError("illegal value entered for a or m or n")

    lenM : int = m.bit_length() # LEN OF M IN BITS
    res : int = 1 

    for j in range(lenM): # iter over all bits
        tempA : int = a
        if (m & (1 << j)): # if bj == 1
            for i in range(j):
                tempA = (tempA * tempA) % n
            res = ( res * tempA) % n
    return res


# M_C as ascii integer code
# param n = p * q, not tot(n)
def enc_dec_singleChar(M_C : int, e_d : int, n : int) -> int: 
    return (modExponent(M_C, e_d, n))


def rsa_word(Message: str, key : int, n : int) -> str:
    ret : str = ""
    for i in range(len(Message)):
        ret += chr(enc_dec_singleChar(ord(Message[i]), key, n))
    
    return ret


# FUNCTION BELOW TAKEN FROM : https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
    # modified by Emre Eser
# returns a^-1 (mod n)
# Algorithm Assumption: a and n are coprimes
def modInverse(a : int, n : int) -> int:

    if (eu_th.gcd(a, n) != 1):
        raise Exception(f"{a} and {n} are not coprimes")

    m0 = n
    y = 0
    x = 1
 
    if (n == 1):
        return 0
 
    while (a > 1):
 
        # q is quotient
        q = a // n
 
        t = n
 
        # m is remainder now, process
        # same as Euclid's algo
        n = a % n
        a = t
        t = y
 
        # Update x and y
        y = x - q * y
        x = t
 
    # Make x positive
    if (x < 0):
        x = x + m0
 
    return x


# suitable d: must be rel. prime to totient(n = p * q)
def findSuitableD(p : int, q : int) -> int:
    compBase : int = max(p,q) + ( (1) if (p == 2 or q == 2) else (2) )

    while(True):
        for i in range(3, compBase):
            if (eu_th.gcd(i, compBase) != 1):
                compBase += 2
                continue
        return compBase
import euler_theorem as eu_th
from typing import List


def sizeInBits(n : int, begin : int = 7) -> int:
    for i in range(begin + 1): # 0 to (and inc.) begin
        if (n >= (1 << (begin - i) )): 
            return i + 1
    return 0


# calculates: a^m mod n
def modExponent(a : int, m : int, n: int) -> int: # algorithm due Diadel
    if (a <= 0 or m < 0 or n <= 1):
        raise ValueError("illegal value entered for a or m or n")

    lenM : int = sizeInBits(m) # LEN OF M IN BITS
    res : int = 1 

    for j in range(lenM): # iter over all bits
        tempA : int = a
        if (m & (1 << j)): # if bj == 1
            for i in range(j):
                tempA = (tempA * tempA) % n
            res = (res * tempA) % n
    return res


# M_C in ascii
def enc_dec_singleChar(M_C : int, e_d : int, n : int) -> int: 
    return (modExponent(M_C, e_d, n))



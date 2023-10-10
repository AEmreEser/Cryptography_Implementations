from math import pow
from typing import List, Tuple

def alph_ord(ch : str):
    return ch - 'a'

def alph_ord_cap(ch : str):
    return ch - 'A'


def enc(key : Tuple[int, int], ptext : str, ring_size : int):
    ctext : str = ''

    for i in len(ptext):
        ctext += ((  (key[0] * alph_ord(ptext)) % ring_size + (key[1]) ) % ring_size)
    
    return ctext

def dec(key : Tuple[int, int], ctext : str, ring_size: int ):
    ptext : str = ''

    for i in len(ctext):
        ptext += (  ((ctext - tuple[1]) % ring_size) * (pow(key[0], -1, ring_size))  ) % ring_size
from math import pow as mpow # math pow and builtin pow are different
from typing import List, Tuple

def alph_ord(ch : str):
    return ord(ch) - ord('a')
    
def alph_ord_cap(ch : str):
    return ord(ch) - 'A'
    

def enc(key : Tuple[int, int], ptext : str, ring_size : int):
    ctext : str = ''

    for i in range(len(ptext)):
        ctext += chr( ord('a') + ((  (key[0] * alph_ord(ptext[i])) % ring_size + (key[1]) ) % ring_size) )
    
    return ctext

def dec(key : Tuple[int, int], ctext : str, ring_size: int ):
    ptext : str = ''

    for i in range(len(ctext)):
        ptext += chr(((  ((alph_ord(ctext[i]) - key[1]) % ring_size) * (pow(key[0], -1, ring_size))  ) % ring_size) + ord('a') )
    return ptext
from typing import Tuple, List
from affine_lib import *
from sys import argv, argc

def __main__():
    ptext :str = 'abcd'
    key :Tuple[int, int] = (3, 7)
    rsize: int = 26
    ctext = enc(key, ptext, rsize) 
    print(ctext)
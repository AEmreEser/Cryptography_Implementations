#!/bin/python3
from typing import Tuple, List
from random import randint, Random, seed
from affine_lib import *
from sys import argv

ptext : str = 'abcd'
key : Tuple[int, int] = (3, 7)
rsize = 26

key : Tuple[int, int] = (Random().randint(1, 25), Random().randint(1, 25)) # 1 - 25: 1 to prevent it from becoming a shift cipher

print("key =",key)

for i in range(rsize):
    test_ch = chr( i + ord('a'))

    try:
        assert(test_ch == dec(key, enc(key, test_ch, rsize), rsize))
    except AssertionError:
        print("ch = ", test_ch, i)
        exit(1)

print("all test passed!")
exit(0)
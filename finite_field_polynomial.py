from typing import List
import finite_field as finField


class PolynFiniteField:
    primeBaseOfField : int # p
    dimensionOfField : int # n

    def __init__(self, n: int = 3, p : int = 2):
        self.primeBaseOfField = p
        self.dimensionOfField = n
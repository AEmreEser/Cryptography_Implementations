from typing import List

class FiniteField:

    dimensionOfField: int
    # Need to make this final

    multiplicationTable: List[List[int]] = None

    # returns None for inverse not founc
    def getMultInverse(self, entry: int) -> int: # NOT READY
        entry = entry % self.dimensionOfField
        
        for i in range(self.dimensionOfField):
            temp = self.multiplicationTable[entry][i]
            if (temp == 1):
                return i
        return None

    def __init__(self, dim: int = 2):
        self.dimensionOfField = dim
        self.multiplicationTable = []

    def generate_mult_table(self) -> None:
        for i in range(self.dimensionOfField): 
            tempTable : List[int] = []
            for j in range(self.dimensionOfField):
                tempTable.append(( (i) * (j) ) % self.dimensionOfField)
            self.multiplicationTable.append(tempTable)

    def printMultTable(self) -> None:
        for i in range(self.dimensionOfField):
            for j in range(self.dimensionOfField):
                print(self.multiplicationTable[i][j], end="\t")
            print('\n')
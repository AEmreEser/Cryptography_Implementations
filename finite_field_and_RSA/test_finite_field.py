import finite_field_and_RSA.finite_field as finField

fourWay = finField.FiniteField(11)

fourWay.generate_mult_table()

fourWay.printMultTable()

print( fourWay.getMultInverse(13) )
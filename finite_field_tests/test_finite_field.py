import finite_field_tests.finite_field as finField

fourWay = finField.FiniteField(11)

fourWay.generate_mult_table()

fourWay.printMultTable()

print( fourWay.getMultInverse(13) )
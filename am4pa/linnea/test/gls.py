def generalized_least_squares(m=2500,n=500):

    b = Vector("b", (n, 1))

    X = Matrix("X", (m, n))
    X.set_property(Property.FULL_RANK)

    M = Matrix("M", (m, m))
    M.set_property(Property.SPD)

    y = Vector("y", (m, 1))

    # b = (X.T*M.inv*X).inv*X.T*M.inv*y
    equations = Equations(Equal(b, Times(Inverse(Times(Transpose(X), Inverse(M), X)), Transpose(X), Inverse(M), y)))

    return equations
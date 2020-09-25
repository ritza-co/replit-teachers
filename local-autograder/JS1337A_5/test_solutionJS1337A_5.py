import mainJS1337A_5 as main



def test_add_two_pos():
    assert main.add(1,2) == 3

def test_add_one_neg_one_pos():
    assert main.add(-3, 1) == -2

def test_subtract_two_pos():
    assert main.subtract(5, 3) == 2

def test_subtract_two_neg():
    assert main.subtract(-2, -3) == 1

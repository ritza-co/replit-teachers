# Ensure the above line contains exactly your student number.
# 
# You can test your code by pressing the run button. 
# Once you are happy with it, uncomment the "`MODE = "SUBMIT"` line 
# and press the Run button again to submit
# -----------------------------------------------------------------

MODE = "TEST"
MODE = "SUBMIT"

def add(a, b):
    """Add a and b and return the sum"""
    return a + b

def subtract(a, b):
    """Subtract b from a and return the result"""
    return b - a

def test():
    r = add(1, 2)
    print(f'add(1, 2) returns {r}')
    r = subtract(5, 2)
    print(f'subtract(5, 2) returns {r}')

def main():
    if MODE == "SUBMIT":
        from submit import submit
        submit()
    else:
        test()

if __name__ == "__main__":
    main()

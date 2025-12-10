import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.calculator import Calculator


def test_add():
    assert Calculator.add(2, 3) == 5

def test_subtract():
    assert Calculator.subtract(5, 3) == 2

def test_multiply():
    assert Calculator.multiply(2, 3) == 6

def test_divide():
    assert Calculator.divide(10, 2) == 5


if __name__ == "__main__":
    # Run all tests manually
    try:
        test_add()
        test_subtract()
        test_multiply()
        test_divide()
        print(" All calculator tests passed successfully!")
    except AssertionError:
        print(" A test failed.")

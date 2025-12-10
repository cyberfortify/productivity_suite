from modules.utils import (
    print_header,
    get_float_input,
    get_int_input,
    pause,
)


class Calculator:
    """Simple calculator with basic arithmetic operations."""

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b


def get_two_numbers():
    """Helper to get two numbers from user."""
    num1 = get_float_input("Enter first number: ")
    num2 = get_float_input("Enter second number: ")
    return num1, num2


def run_calculator():
    """Run the calculator tool with a menu."""
    calc = Calculator()

    while True:
        print_header("CALCULATOR TOOL")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Back to Main Menu")
        print()

        choice = get_int_input("Enter your choice (1-5): ", min_value=1, max_value=5)

        if choice == 5:
            # Back to main menu
            break

        try:
            num1, num2 = get_two_numbers()

            if choice == 1:
                result = calc.add(num1, num2)
                operation = "+"
            elif choice == 2:
                result = calc.subtract(num1, num2)
                operation = "-"
            elif choice == 3:
                result = calc.multiply(num1, num2)
                operation = "*"
            elif choice == 4:
                result = calc.divide(num1, num2)
                operation = "/"
            else:
                print("Invalid choice.")
                pause()
                continue

            print(f"\nResult: {num1} {operation} {num2} = {result}")
        except ZeroDivisionError as e:
            print(f"\nError: {e}")

        pause()

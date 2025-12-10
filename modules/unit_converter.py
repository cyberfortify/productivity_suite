# modules/unit_converter.py

from modules.utils import print_header, get_float_input, get_int_input, pause


def convert_length():
    """Convert length units (meter, kilometer, centimeter)."""
    print_header("UNIT CONVERTER - LENGTH")
    print("1. Meters to Kilometers")
    print("2. Kilometers to Meters")
    print("3. Meters to Centimeters")
    print("4. Centimeters to Meters")
    print("5. Back")
    print()

    choice = get_int_input("Enter choice (1-5): ", min_value=1, max_value=5)

    if choice == 5:
        return

    value = get_float_input("Enter value: ")

    if choice == 1:
        result = value / 1000
        print(f"{value} meters = {result} kilometers")
    elif choice == 2:
        result = value * 1000
        print(f"{value} kilometers = {result} meters")
    elif choice == 3:
        result = value * 100
        print(f"{value} meters = {result} centimeters")
    elif choice == 4:
        result = value / 100
        print(f"{value} centimeters = {result} meters")

    pause()


def convert_weight():
    """Convert weight units (kg, grams)."""
    print_header("UNIT CONVERTER - WEIGHT")
    print("1. Kilograms to Grams")
    print("2. Grams to Kilograms")
    print("3. Back")
    print()

    choice = get_int_input("Enter choice (1-3): ", min_value=1, max_value=3)

    if choice == 3:
        return

    value = get_float_input("Enter value: ")

    if choice == 1:
        result = value * 1000
        print(f"{value} kg = {result} grams")
    elif choice == 2:
        result = value / 1000
        print(f"{value} grams = {result} kg")

    pause()


def convert_temperature():
    """Convert temperature units (Celsius, Fahrenheit)."""
    print_header("UNIT CONVERTER - TEMPERATURE")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Back")
    print()

    choice = get_int_input("Enter choice (1-3): ", min_value=1, max_value=3)

    if choice == 3:
        return

    value = get_float_input("Enter value: ")

    if choice == 1:
        result = (value * 9 / 5) + 32
        print(f"{value} °C = {result} °F")
    elif choice == 2:
        result = (value - 32) * 5 / 9
        print(f"{value} °F = {result} °C")

    pause()


def run_unit_converter():
    """Main menu for unit converter."""
    while True:
        print_header("UNIT CONVERTER")
        print("1. Length")
        print("2. Weight")
        print("3. Temperature")
        print("4. Back to Main Menu")
        print()

        choice = get_int_input("Enter choice (1-4): ", min_value=1, max_value=4)

        if choice == 1:
            convert_length()
        elif choice == 2:
            convert_weight()
        elif choice == 3:
            convert_temperature()
        elif choice == 4:
            break

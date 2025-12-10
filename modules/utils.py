import os
from datetime import datetime

APP_NAME = "PERSONAL PRODUCTIVITY SUITE"
APP_VERSION = "v1.0.0"


def clear_screen():
    """Clear the terminal screen."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pause():
    """Wait for user to press Enter."""
    input("\nPress Enter to continue...")


def print_header(title: str):
    """Print a formatted header with a title."""
    clear_screen()
    print("=" * 42)
    print(title.center(42))
    print("=" * 42)
    print()


def print_banner():
    """Print app banner once (name + version)."""
    clear_screen()
    print("=" * 42)
    print(APP_NAME.center(42))
    print(APP_VERSION.center(42))
    print("=" * 42)
    print()


def get_int_input(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """
    Safely get an integer input from user with optional range.
    Handles invalid inputs gracefully.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a value >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a value <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_float_input(prompt: str, min_value: float = None, max_value: float = None) -> float:
    """
    Safely get a float input from user with optional range.
    Handles invalid inputs gracefully.
    """
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a value >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a value <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number (integer or decimal).")


def get_non_empty_input(prompt: str) -> str:
    """
    Get non-empty string input from user.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_timestamp() -> str:
    """Return current timestamp as string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def confirm_action(message: str) -> bool:
    """
    Ask user to confirm an action with (y/n).
    Returns True if confirmed.
    """
    while True:
        ans = input(f"{message} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")

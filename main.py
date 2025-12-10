from modules.utils import (
    print_header,
    print_banner,
    get_int_input,
    pause,
)
from modules.calculator import run_calculator
from modules.notes_manager import run_notes_manager
from modules.timer import run_timer
from modules.file_organizer import run_file_organizer
from modules.unit_converter import run_unit_converter
from modules.backup_manager import run_backup_manager


def show_main_menu():
    """Display the main menu of the Productivity Suite."""
    print_header("PERSONAL PRODUCTIVITY SUITE")

    print("MAIN MENU:")
    print("1. Calculator Tool")
    print("2. Notes Manager")
    print("3. Timer & Stopwatch")
    print("4. File Organizer")
    print("5. Unit Converter")
    print("6. Backup & Restore")
    print("7. Exit")
    print()

    choice = get_int_input("Enter your choice (1-7): ", min_value=1, max_value=7)
    return choice


def main():
    """Main loop of the application."""
    # Show banner once at start
    print_banner()
    pause()

    while True:
        choice = show_main_menu()

        if choice == 1:
            run_calculator()
        elif choice == 2:
            run_notes_manager()
        elif choice == 3:
            run_timer()
        elif choice == 4:
            run_file_organizer()
        elif choice == 5:
            run_unit_converter()
        elif choice == 6:
            run_backup_manager()
        elif choice == 7:
            print("\nExiting Personal Productivity Suite. Goodbye!")
            break


if __name__ == "__main__":
    main()

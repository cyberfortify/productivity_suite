# modules/backup_manager.py

import os
import shutil
from datetime import datetime

from modules.utils import print_header, get_int_input, confirm_action, pause


DATA_FOLDER = "data"
BACKUP_FOLDER = os.path.join(DATA_FOLDER, "backups")

# Kaun se files ka backup lena hai:
FILES_TO_BACKUP = [
    os.path.join(DATA_FOLDER, "notes.json"),
    # future me aur bhi files yahan add kar sakte ho
]


def ensure_backup_folder():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER, exist_ok=True)


def create_backup():
    """Create a timestamped backup of data files."""
    ensure_backup_folder()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

    copied_files = 0

    for file_path in FILES_TO_BACKUP:
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_dir)
            copied_files += 1

    if copied_files == 0:
        print("\nℹ️ No data files found to backup.")
    else:
        print(f"\n✅ Backup created at: {backup_dir}")
        print(f"Total files backed up: {copied_files}")


def list_backups():
    """List all available backups."""
    ensure_backup_folder()

    backups = [
        d for d in os.listdir(BACKUP_FOLDER)
        if os.path.isdir(os.path.join(BACKUP_FOLDER, d))
    ]
    backups.sort()

    if not backups:
        print("\nℹ️ No backups available.")
        return []

    print("\nAvailable Backups:")
    for idx, name in enumerate(backups, start=1):
        print(f"{idx}. {name}")

    return backups


def restore_backup():
    """Restore data from a selected backup."""
    backups = list_backups()
    if not backups:
        return

    choice = get_int_input(
        "\nEnter backup number to restore (0 to cancel): ",
        min_value=0,
        max_value=len(backups),
    )

    if choice == 0:
        print("Restore cancelled.")
        return

    backup_name = backups[choice - 1]
    backup_path = os.path.join(BACKUP_FOLDER, backup_name)

    print(f"\nYou selected backup: {backup_name}")
    if not confirm_action("This will overwrite current data files. Continue?"):
        print("Restore cancelled.")
        return

    restored_files = 0
    for file_name in os.listdir(backup_path):
        src = os.path.join(backup_path, file_name)
        dst = os.path.join(DATA_FOLDER, file_name)
        shutil.copy2(src, dst)
        restored_files += 1

    print(f"\n✅ Restore completed. Files restored: {restored_files}")


def run_backup_manager():
    """Backup & Restore menu."""
    while True:
        print_header("BACKUP & RESTORE")
        print("1. Create Backup")
        print("2. List Backups")
        print("3. Restore Backup")
        print("4. Back to Main Menu")
        print()

        choice = get_int_input("Enter choice (1-4): ", min_value=1, max_value=4)

        if choice == 1:
            create_backup()
            pause()
        elif choice == 2:
            list_backups()
            pause()
        elif choice == 3:
            restore_backup()
            pause()
        elif choice == 4:
            break

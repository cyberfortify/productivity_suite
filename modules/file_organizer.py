import os
import shutil
from pathlib import Path

from modules.utils import (
    print_header,
    get_non_empty_input,
    get_int_input,
    pause,
)


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mov", ".mkv"],
    "Music": [".mp3", ".wav"],
    "Code": [".py", ".js", ".html"],
}


def organize_files(target_folder: str):
    """
    Organize files in the target folder into subfolders based on file extension.
    """
    target = Path(target_folder).expanduser()

    if not target.exists():
        print("\n Folder does not exist.")
        return

    if not target.is_dir():
        print("\n Given path is not a folder.")
        return

    files_moved = 0

    for file in target.iterdir():
        if file.is_file():
            ext = file.suffix.lower()

            moved = False
            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    dst_folder = target / folder
                    dst_folder.mkdir(exist_ok=True)
                    shutil.move(str(file), str(dst_folder / file.name))
                    moved = True
                    files_moved += 1
                    break

            if not moved:
                other_folder = target / "Others"
                other_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(other_folder / file.name))
                files_moved += 1

    if files_moved == 0:
        print("\n No files to organize in this folder.")
    else:
        print(f"\n Files organized successfully! Total files moved: {files_moved}")


def run_file_organizer():
    """
    File organizer menu
    """
    while True:
        print_header("FILE ORGANIZER")

        print("1. Organize current folder")
        print("2. Enter custom folder path")
        print("3. Back to Main Menu")
        print()

        choice = get_int_input("Enter choice (1-3): ", min_value=1, max_value=3)

        if choice == 1:
            organize_files(".")
            pause()

        elif choice == 2:
            path = get_non_empty_input("Enter folder path: ")
            organize_files(path)
            pause()

        elif choice == 3:
            break

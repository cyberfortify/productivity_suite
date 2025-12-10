import json
import os
from datetime import datetime

from modules.utils import (
    print_header,
    get_non_empty_input,
    get_int_input,
    pause,
)


class NotesManager:
    """Manages notes with JSON file persistence."""

    def __init__(self, file_path: str = None):
        self.file_path = file_path or os.path.join("data", "notes.json")
        self.notes = []
        self.load_notes()

    def load_notes(self):
        """Load notes from JSON file."""
        try:
            if not os.path.exists("data"):
                os.makedirs("data", exist_ok=True)

            with open(self.file_path, "r", encoding="utf-8") as f:
                self.notes = json.load(f)
        except FileNotFoundError:
            self.notes = []
        except json.JSONDecodeError:
            print("Warning: notes.json is corrupted. Resetting notes.")
            self.notes = []

    def save_notes(self):
        """Save notes to JSON file."""
        if not os.path.exists("data"):
            os.makedirs("data", exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, indent=2, ensure_ascii=False)

    def add_note(self, title: str, content: str) -> str:
        """Add a new note."""
        note = {
            "id": len(self.notes) + 1,
            "title": title,
            "content": content,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.notes.append(note)
        self.save_notes()
        return f"Note '{title}' added successfully! (ID: {note['id']})"

    def list_notes(self):
        """Return list of notes."""
        return self.notes

    def find_note_by_id(self, note_id: int):
        """Find a note by its ID."""
        for note in self.notes:
            if note["id"] == note_id:
                return note
        return None

    def search_notes(self, keyword: str):
        """Search notes by keyword in title or content."""
        keyword_lower = keyword.lower()
        return [
            note
            for note in self.notes
            if keyword_lower in note["title"].lower()
            or keyword_lower in note["content"].lower()
        ]

    def edit_note(self, note_id: int, new_title: str = None, new_content: str = None):
        """Edit an existing note."""
        note = self.find_note_by_id(note_id)
        if not note:
            return False

        if new_title:
            note["title"] = new_title
        if new_content:
            note["content"] = new_content

        note["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_notes()
        return True

    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID."""
        note = self.find_note_by_id(note_id)
        if not note:
            return False

        self.notes.remove(note)
        
        for idx, n in enumerate(self.notes, start=1):
            n["id"] = idx

        self.save_notes()
        return True

    def export_notes_to_txt(self, export_path: str = None):
        """Export all notes to a TXT file."""
        if export_path is None:
            export_path = os.path.join("data", "notes_export.txt")

        lines = []
        for note in self.notes:
            lines.append(f"ID: {note['id']}")
            lines.append(f"Title: {note['title']}")
            lines.append(f"Created: {note['created']}")
            lines.append(f"Modified: {note['modified']}")
            lines.append("Content:")
            lines.append(note["content"])
            lines.append("-" * 40)

        with open(export_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return export_path

    def export_notes_to_csv(self, export_path: str = None):
        """Export notes to a CSV file."""
        import csv

        if export_path is None:
            export_path = os.path.join("data", "notes_export.csv")

        fieldnames = ["id", "title", "content", "created", "modified"]
        with open(export_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow(note)

        return export_path


def display_notes(notes):
    """Pretty-print notes list."""
    if not notes:
        print("No notes found.")
        return

    print("-" * 60)
    for note in notes:
        print(f"ID: {note['id']}")
        print(f"Title: {note['title']}")
        print(f"Created: {note['created']}")
        print(f"Modified: {note['modified']}")
        print("Content:")
        print(note["content"])
        print("-" * 60)


def run_notes_manager():
    """Run the notes manager with its own menu."""
    manager = NotesManager()

    while True:
        print_header("NOTES MANAGER")
        print("1. View All Notes")
        print("2. Add New Note")
        print("3. Search Notes")
        print("4. Edit Note")
        print("5. Delete Note")
        print("6. Export Notes")
        print("7. Back to Main Menu")
        print()

        choice = get_int_input("Enter choice (1-7): ", min_value=1, max_value=7)

        if choice == 1:
            # View all notes
            display_notes(manager.list_notes())
            pause()

        elif choice == 2:
            
            print_header("ADD NEW NOTE")
            title = get_non_empty_input("Enter note title: ")
            print("Enter note content (end with an empty line):")
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            content = "\n".join(lines)

            message = manager.add_note(title, content)
            print("\n", message)
            pause()

        elif choice == 3:
            
            print_header("SEARCH NOTES")
            keyword = get_non_empty_input("Enter keyword to search: ")
            results = manager.search_notes(keyword)
            display_notes(results)
            pause()

        elif choice == 4:
            
            print_header("EDIT NOTE")
            display_notes(manager.list_notes())
            if not manager.list_notes():
                pause()
                continue

            note_id = get_int_input("Enter Note ID to edit: ", min_value=1)
            note = manager.find_note_by_id(note_id)
            if not note:
                print("No note found with that ID.")
                pause()
                continue

            print(f"\nCurrent title: {note['title']}")
            new_title = input("Enter new title (leave blank to keep same): ").strip()
            print("\nCurrent content:")
            print(note["content"])
            print("\nEnter new content (leave blank to keep same, end with empty line):")
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            new_content = "\n".join(lines).strip()

            updated = manager.edit_note(
                note_id,
                new_title=new_title or None,
                new_content=new_content or None,
            )
            if updated:
                print("\nNote updated successfully.")
            else:
                print("\nFailed to update note.")
            pause()

        elif choice == 5:
            
            print_header("DELETE NOTE")
            display_notes(manager.list_notes())
            if not manager.list_notes():
                pause()
                continue

            note_id = get_int_input("Enter Note ID to delete: ", min_value=1)
            confirm = input(
                f"Are you sure you want to delete note {note_id}? (y/n): "
            ).strip().lower()
            if confirm == "y":
                if manager.delete_note(note_id):
                    print("Note deleted successfully.")
                else:
                    print("No note found with that ID.")
            else:
                print("Deletion cancelled.")
            pause()

        elif choice == 6:
            
            print_header("EXPORT NOTES")
            print("1. Export to TXT")
            print("2. Export to CSV")
            print("3. Cancel")
            print()
            export_choice = get_int_input("Enter choice (1-3): ", min_value=1, max_value=3)
            if export_choice == 1:
                path = manager.export_notes_to_txt()
                print(f"\n Notes exported to: {path}")
            elif export_choice == 2:
                path = manager.export_notes_to_csv()
                print(f"\n Notes exported to: {path}")
            else:
                print("\nExport cancelled.")
            pause()

        elif choice == 7:
            break

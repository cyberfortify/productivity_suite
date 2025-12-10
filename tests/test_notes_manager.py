import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from modules.notes_manager import NotesManager


def test_add_note():
    manager = NotesManager(file_path="data/test_notes.json")
    result = manager.add_note("Test Title", "Test Content")

    assert "added successfully" in result.lower()
    assert len(manager.notes) >= 1


if __name__ == "__main__":
    try:
        test_add_note()
        print(" NotesManager test passed successfully!")
    except AssertionError:
        print(" NotesManager test failed.")

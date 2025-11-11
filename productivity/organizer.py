from pathlib import Path
import shutil

def organize_folder(source: str, dry_run: bool = True):
    p = Path(source).expanduser()
    if not p.exists() or not p.is_dir():
        raise ValueError("Source must be an existing directory.")
    actions = []
    for child in p.iterdir():
        if child.is_file():
            ext = child.suffix.lower().lstrip('.')
            target_dir = p / (ext or "no_ext")
            actions.append((child, target_dir))
    if dry_run:
        return actions
    for src, tgt in actions:
        tgt.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(tgt / src.name))
    return actions

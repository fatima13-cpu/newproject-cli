#!/usr/bin/env python3
"""
organize — a simple CLI that sorts a messy folder (like Downloads) into
sub-folders based on file type, so nothing stays randomly scattered.

USAGE:
    organize C:\\Users\\Fatima\\Downloads
    organize C:\\Users\\Fatima\\Downloads --dry-run

WHAT IT DOES:
    Scans the given folder (top level only, not sub-folders) and moves
    each file into a category folder based on its extension:

        Downloads/
            Images/        (.jpg, .png, .gif, ...)
            PDFs/          (.pdf)
            Documents/     (.docx, .txt, ...)
            Spreadsheets/  (.xlsx, .csv, ...)
            Archives/      (.zip, .rar, ...)
            Audio/         (.mp3, .wav, ...)
            Video/         (.mp4, .mkv, ...)
            Code/          (.py, .cpp, .js, ...)
            Executables/   (.exe, .msi)
            Others/        (anything unrecognized)

    --dry-run shows what WOULD happen without moving anything — always
    safe to run first to check before actually organizing.
"""

import argparse
import sys
from pathlib import Path


# ---------------------------------------------------------
# 1. CONFIG — extension -> category folder name
# ---------------------------------------------------------
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx", ".txt", ".odt", ".rtf"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Video": [".mp4", ".mkv", ".avi", ".mov"],
    "Code": [".py", ".cpp", ".c", ".java", ".js", ".html", ".css", ".asm"],
    "Executables": [".exe", ".msi"],
}

ALL_CATEGORY_NAMES = set(CATEGORIES.keys()) | {"Others"}


def category_for(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


# ---------------------------------------------------------
# 2. THE ACTUAL LOGIC
# ---------------------------------------------------------
def plan_moves(folder: Path):
    """
    Looks at every file directly inside `folder` (skips sub-folders,
    including category folders from a previous run) and returns a list
    of (source_path, destination_folder_name) pairs.
    """
    moves = []
    for item in folder.iterdir():
        if item.is_dir():
            continue  # don't touch existing folders, including our own category folders
        if item.name.startswith("."):
            continue  # skip hidden files
        category = category_for(item.suffix)
        moves.append((item, category))
    return moves


def unique_destination(dest_folder: Path, filename: str) -> Path:
    """
    If a file with the same name already exists in the destination,
    append (1), (2), etc. instead of overwriting it.
    """
    dest = dest_folder / filename
    if not dest.exists():
        return dest

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        candidate = dest_folder / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def execute_moves(moves, folder: Path):
    moved_count = 0
    for src, category in moves:
        dest_folder = folder / category
        dest_folder.mkdir(exist_ok=True)
        dest = unique_destination(dest_folder, src.name)
        src.rename(dest)
        moved_count += 1
    return moved_count


# ---------------------------------------------------------
# 3. CLI PARSING
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Sort a messy folder into sub-folders by file type."
    )
    parser.add_argument("folder", help="Folder to organize, e.g. Downloads")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without actually moving any files",
    )

    args = parser.parse_args()
    folder = Path(args.folder).expanduser().resolve()

    if not folder.exists() or not folder.is_dir():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)

    moves = plan_moves(folder)

    if not moves:
        print("✅ Nothing to organize — folder is already clean (or empty).")
        return

    if args.dry_run:
        print(f"🔎 Dry run — nothing will actually be moved.\n")
        for src, category in moves:
            print(f"   {src.name}  ->  {category}/")
        print(f"\n({len(moves)} file(s) would be organized. Run without --dry-run to actually do it.)")
    else:
        moved_count = execute_moves(moves, folder)
        print(f"✅ Organized {moved_count} file(s) in {folder}")
        used_categories = sorted(set(cat for _, cat in moves))
        for cat in used_categories:
            print(f"   ├── {cat}/")


if __name__ == "__main__":
    main()

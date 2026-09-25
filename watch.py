#!/usr/bin/env python3
"""
watch — automatically organizes a folder in real time, in the background.

Unlike `organize` (which you run manually whenever you want to tidy up),
`watch` runs continuously and moves each new file into the right
category folder (Images, PDFs, Documents, etc) the moment it appears —
so Downloads never gets messy in the first place.

USAGE:
    watch C:\\Users\\Fatima\\Downloads

Leave this running in its own terminal window (minimize it, don't close
it). Press Ctrl+C in that window to stop watching.

Uses the exact same categories/logic as `organize.py` — this file must
stay in the same folder as organize.py to work.
"""

import argparse
import sys
import time
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ This tool needs the 'watchdog' package. Install it with:")
    print("   pip install watchdog")
    sys.exit(1)

# Reuse the same categorization logic as `organize`, so both tools
# always behave identically
from organize import category_for, unique_destination


class OrganizeHandler(FileSystemEventHandler):
    # Extensions browsers use for in-progress downloads — never touch these
    TEMP_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}

    def __init__(self, folder: Path):
        self.folder = folder

    def on_created(self, event):
        if event.is_directory:
            return
        self._handle_new_file(Path(event.src_path))

    def on_moved(self, event):
        # Browsers download to a temp name (e.g. file.pdf.crdownload) then
        # RENAME it to the final name once done — that rename fires this
        # event, not on_created, so we need to handle it too.
        if event.is_directory:
            return
        self._handle_new_file(Path(event.dest_path))

    def _handle_new_file(self, src: Path):
        # Skip temp/in-progress download files entirely
        if src.suffix.lower() in self.TEMP_EXTENSIONS:
            return

        # Only react to files landing directly in the watched folder,
        # not files already inside a category sub-folder
        if src.parent != self.folder:
            return

        # Give the file a moment to finish being written before we move it
        time.sleep(1)

        if not src.exists():
            return  # was likely a temporary/partial download file

        category = category_for(src.suffix)
        dest_folder = self.folder / category
        dest_folder.mkdir(exist_ok=True)
        dest = unique_destination(dest_folder, src.name)

        try:
            src.rename(dest)
            print(f"✅ Moved: {src.name}  ->  {category}/")
        except (PermissionError, FileNotFoundError):
            # File might still be downloading/locked by the browser —
            # skip silently; running `organize` manually later will catch it
            pass


def main():
    parser = argparse.ArgumentParser(
        description="Watch a folder and automatically organize new files as they arrive."
    )
    parser.add_argument("folder", help="Folder to watch, e.g. Downloads")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()

    if not folder.exists() or not folder.is_dir():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)

    print(f"👀 Watching {folder}")
    print("   New files will be organized automatically as they arrive.")
    print("   Press Ctrl+C to stop.\n")

    event_handler = OrganizeHandler(folder)
    observer = Observer()
    observer.schedule(event_handler, str(folder), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Stopped watching.")
    observer.join()


if __name__ == "__main__":
    main()

# CLI Toolkit

A small collection of command-line tools I built to automate repetitive parts of my student/dev workflow — project setup and file organization. Each one is a standalone Python script with its own `.bat` wrapper so it can be run as a normal command from anywhere.

## Tools

### 1. `newproject` — assignment folder generator

Creates a standardized project folder (with the right structure for C++ or Assembly/COAL courses) and initializes a git repo, in one command.

```
newproject dsa_assignment5 --course DSA
newproject asm_lab2 --course COAL
```

### 2. `organize` — file organizer (manual)

Sorts a messy folder (like Downloads) into sub-folders by file type (Images, PDFs, Documents, Archives, etc). Supports a safe `--dry-run` preview before actually moving anything. Run this whenever you want to tidy up.

```
organize C:\Users\you\Downloads --dry-run
organize C:\Users\you\Downloads
```

### 3. `watch` — file organizer (automatic)

Same categorization logic as `organize`, but runs continuously in the background and organizes each file the moment it appears — so the folder never gets messy in the first place. Requires the `watchdog` package (`pip install watchdog`).

```
watch C:\Users\you\Downloads
```

Leave it running in its own terminal window; press Ctrl+C to stop.

## Installation (Windows)

1. Clone this repo, or download the files, into a permanent folder (e.g. `C:\Tools`)
2. Add that folder to your system PATH (System Properties → Environment Variables → Path → New → add the folder path)
3. Run `pip install watchdog` (only needed for the `watch` command)
4. Open a new terminal — all commands (`newproject`, `organize`, `watch`) now work from any folder

## Why I built these

As a student juggling multiple courses (C++, COAL/Assembly, and general coursework), I kept running into the same friction points: scattered assignment folders and a messy Downloads folder. Each tool automates one specific piece of that friction — `organize` for on-demand cleanup, `watch` for real-time, hands-off organizing — instead of trying to do everything in one bloated script.

## Tech

Built in Python using only the standard library (`argparse`, `pathlib`, `difflib`, `subprocess`) — no external dependencies required. Each tool separates its core logic from its CLI-parsing layer, so the logic can be tested or reused independently of the terminal.

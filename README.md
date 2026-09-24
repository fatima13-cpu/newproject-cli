# CLI Toolkit

A small collection of command-line tools I built to automate repetitive parts of my student/dev workflow — project setup, file organization, and text comparison. Each one is a standalone Python script with its own `.bat` wrapper so it can be run as a normal command from anywhere.

## Tools

### 1. `newproject` — assignment folder generator

Creates a standardized project folder (with the right structure for C++ or Assembly/COAL courses) and initializes a git repo, in one command.

```
newproject dsa_assignment5 --course DSA
newproject asm_lab2 --course COAL
```

### 2. `organize` — file organizer

Sorts a messy folder (like Downloads) into sub-folders by file type (Images, PDFs, Documents, Archives, etc). Supports a safe `--dry-run` preview before actually moving anything.

```
organize C:\Users\you\Downloads --dry-run
organize C:\Users\you\Downloads
```

## Installation (Windows)

1. Clone this repo, or download the files, into a permanent folder (e.g. `C:\Tools`)
2. Add that folder to your system PATH (System Properties → Environment Variables → Path → New → add the folder path)
3. Open a new terminal — both commands (`newproject`, `organize`) now work from any folder

## Why I built these

As a student juggling multiple courses (C++, COAL/Assembly, and general coursework), I kept running into the same friction points: scattered assignment folders and a messy Downloads folder. Each tool automates one specific piece of that friction instead of trying to do everything in one bloated script.

## Tech

Built in Python using only the standard library (`argparse`, `pathlib`, `difflib`, `subprocess`) — no external dependencies required. Each tool separates its core logic from its CLI-parsing layer, so the logic can be tested or reused independently of the terminal.

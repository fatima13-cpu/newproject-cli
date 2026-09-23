# newproject-cli

A simple command-line tool that automatically generates a standardized project folder structure for C++ and Assembly (COAL) assignments — so nothing gets lost or scattered across random folders.

## What it does

Instead of manually creating folders, starter files, and a git repo every time you start a new assignment, just run one command:

```
newproject <project-name> --course <course-name>
```

It automatically:
- Creates a project folder under `~/CppProjects/`
- Picks the right template based on the course:
  - **COAL / Assembly courses** → `asm/` folder + starter `.asm` file
  - **Everything else (C++, OOP, DSA, etc.)** → `src/` + `include/` folders + starter `main.cpp`
- Adds a `tests/` folder
- Generates a `README.md` with build instructions
- Adds a `.gitignore` for build artifacts
- Runs `git init` automatically so every project is version-controlled from the start

## Usage

```
newproject dsa_assignment5 --course DSA
newproject asm_lab2 --course COAL
newproject oop_hw4 --course OOP
```

## Example output

```
✅ Created project 'asm_lab2' at: C:\Users\you\CppProjects\asm_lab2
   ├── asm/asm_lab2.asm
   ├── tests/
   ├── README.md
   └── .gitignore
✅ Initialized git repo
```

## Why I built this

As a student juggling C++ and Assembly (COAL) coursework, I kept losing track of assignment files scattered across random folders, and repeated the same manual setup (folders, starter files, git init) every single time. This tool automates that entire setup into a single command.

## Tech

Built in Python using `argparse` for CLI parsing and `subprocess` for automatic git initialization. Logic is separated from CLI parsing so the core functionality can be tested or reused independently of the terminal interface.

## Installation

1. Clone this repo or download `newproject.py` and `newproject.bat`
2. Place both files in a permanent folder (e.g. `C:\Tools`)
3. Add that folder to your system PATH
4. Run `newproject <name> --course <course>` from anywhere

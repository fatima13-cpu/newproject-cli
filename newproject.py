#!/usr/bin/env python3
"""
newproject — a tiny CLI that creates a standard project folder for your
assignments, so nothing ends up scattered or lost.

USAGE:
    newproject assignment3
    newproject asm_lab2 --course COAL
    newproject oop_hw4 --course OOP

WHAT IT DOES:
    - Creates a project folder under ~/CppProjects/
    - Picks a folder/file template based on --course
        * "coal" (case-insensitive, matches COAL/assembly courses)
            -> asm/ folder + starter .asm file
        * anything else (default)
            -> src/ + include/ folders + starter main.cpp
    - Adds a tests/ folder, README.md, .gitignore
    - Runs `git init` automatically so it's version-controlled from commit 0
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import date

# ---------------------------------------------------------
# 1. CONFIG
# ---------------------------------------------------------
BASE_DIR = Path.home() / "CppProjects"

CPP_MAIN_TEMPLATE = """#include <iostream>

int main() {{
    std::cout << "Hello from {name}!" << std::endl;
    return 0;
}}
"""

ASM_MAIN_TEMPLATE = """; {name}.asm
; COAL / x86 assembly starter

.MODEL SMALL
.STACK 100H

.DATA
    ; declare your variables here

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; your code here

    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
"""

README_TEMPLATE = """# {name}

Course: {course}
Created: {created_date}

## Description
(Write what this assignment is about.)

## How to build
{build_instructions}
"""

GITIGNORE_TEMPLATE = """# Build artifacts
*.o
*.obj
*.exe
*.out
build/
"""

CPP_BUILD_INSTRUCTIONS = """```
g++ src/main.cpp -o {name} -Iinclude
./{name}
```"""

ASM_BUILD_INSTRUCTIONS = """```
(Assemble/link with whatever your COAL course uses, e.g. MASM/emu8086/DOSBox)
```"""


# ---------------------------------------------------------
# 2. TEMPLATE SELECTION
# ---------------------------------------------------------
def is_assembly_course(course: str) -> bool:
    return "coal" in course.lower() or "assembly" in course.lower()


# ---------------------------------------------------------
# 3. THE ACTUAL LOGIC (separate from CLI parsing on purpose)
# ---------------------------------------------------------
def create_project(name: str, course: str):
    project_path = BASE_DIR / name

    if project_path.exists():
        raise FileExistsError(f"Project '{name}' already exists at {project_path}")

    project_path.mkdir(parents=True)
    (project_path / "tests").mkdir()

    if is_assembly_course(course):
        (project_path / "asm").mkdir()
        (project_path / "asm" / f"{name}.asm").write_text(
            ASM_MAIN_TEMPLATE.format(name=name)
        )
        build_instructions = ASM_BUILD_INSTRUCTIONS.format(name=name)
        layout_lines = ["asm/" + name + ".asm", "tests/"]
    else:
        (project_path / "src").mkdir()
        (project_path / "include").mkdir()
        (project_path / "src" / "main.cpp").write_text(
            CPP_MAIN_TEMPLATE.format(name=name)
        )
        build_instructions = CPP_BUILD_INSTRUCTIONS.format(name=name)
        layout_lines = ["src/main.cpp", "include/", "tests/"]

    (project_path / "README.md").write_text(
        README_TEMPLATE.format(
            name=name,
            course=course,
            created_date=date.today(),
            build_instructions=build_instructions,
        )
    )
    (project_path / ".gitignore").write_text(GITIGNORE_TEMPLATE)

    # Git init — don't let a missing/broken git installation crash the whole tool
    try:
        subprocess.run(
            ["git", "init"],
            cwd=project_path,
            capture_output=True,
            check=True,
        )
        git_ok = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        git_ok = False

    return project_path, layout_lines, git_ok


# ---------------------------------------------------------
# 4. CLI PARSING
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Create a new assignment project with a standard folder structure."
    )
    parser.add_argument("name", help="Name of the new project (e.g. assignment3)")
    parser.add_argument(
        "--course",
        default="general",
        help="Course tag, e.g. COAL, OOP (COAL/assembly gets an asm/ template)",
    )

    args = parser.parse_args()

    try:
        path, layout_lines, git_ok = create_project(args.name, args.course)
    except FileExistsError as e:
        print(f"❌ {e}")
        sys.exit(1)

    print(f"✅ Created project '{args.name}' at: {path}")
    for line in layout_lines:
        print(f"   ├── {line}")
    print(f"   ├── README.md")
    print(f"   └── .gitignore")

    if git_ok:
        print("✅ Initialized git repo")
    else:
        print("⚠️  Skipped git init (git not found or failed) — folders were still created fine")


if __name__ == "__main__":
    main()

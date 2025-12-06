#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def create_day(year, day):
    """
    Create a new day directory for Advent of Code.
    
    Args:
        year: The year (e.g., 2024)
        day: The day number (e.g., 1, 2, etc.)
    """
    day_name = f"day{day}"
    
    # Create directory structure
    day_path = Path(f"./src/{year}/{day}")
    day_path.mkdir(parents=True, exist_ok=True)
    
    # Copy template
    template_path = Path("./src/template.py")
    destination = day_path / f"{day_name}.py"
    shutil.copy(template_path, destination)
    
    print(f"Created {day_path}")
    print(f"Copied template to {destination}")
    
    # Uncomment these lines if you want to automatically:
    # - Create input.txt and test.txt files
    # - Open files in VS Code
    
    # (day_path / "input.txt").touch()
    # (day_path / "test.txt").touch()
    os.system(f'code "{destination}"')
    # os.system(f'code "{day_path / "test.txt"}"')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python createDay.py <year> <day>")
        print("Example: python createDay.py 2024 1")
        sys.exit(1)
    
    year = sys.argv[1]
    day = sys.argv[2]
    
    create_day(year, day)

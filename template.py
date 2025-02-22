import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:%(message)s:')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "research/trails.ipynb"
]

def create_folders_and_files(file_list):

    for file_path_str in file_list:
        file_path = Path(file_path_str)
        try:
            # Create directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Create an empty file if it doesn't exist
            if not file_path.exists():
                file_path.touch()
                logging.info(f"Created file: {file_path}")
            else:
                logging.info(f"File already exists: {file_path}")

        except Exception as e:
            logging.error(f"Error creating {file_path}: {e}")

# Example usage:
create_folders_and_files(list_of_files)
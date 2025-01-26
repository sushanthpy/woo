import os
import re

# Define the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Define directories and files to exclude
EXCLUDE_DIRS = {'__pycache__', 'venv', '.git', 'logs', 'data', 'artifacts', 'build', 'dist'}
EXCLUDE_FILES = {'README.md'}

# Define the output file
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'combined_project.py')

# Supported file extensions
SUPPORTED_EXTENSIONS = {'.py'}

def is_file(filename):
    """
    Check if the file is of a supported type and is not in the exclude list.
    """
    _, ext = os.path.splitext(filename)
    return ext in SUPPORTED_EXTENSIONS and filename not in EXCLUDE_FILES

def should_exclude_dir(dirname):
    """
    Check if the directory should be excluded.
    """
    return dirname in EXCLUDE_DIRS

def get_all_supported_files(root_dir):
    """
    Recursively retrieve all supported files from the directory, excluding specified directories and files.
    """
    supported_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]
        for filename in filenames:
            if is_file(filename):
                file_path = os.path.join(dirpath, filename)
                supported_files.append(file_path)
    return supported_files

def concatenate_files(supported_files, output_file):
    """
    Concatenate all supported files into a single output file.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path in supported_files:
            relative_path = os.path.relpath(file_path, PROJECT_ROOT)
            outfile.write(f'\n# ===== Start of {relative_path} =====\n\n')
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
            outfile.write(f'\n# ===== End of {relative_path} =====\n')
    print(f"All files have been concatenated into {output_file}")

def main():
    """
    Main function to get all supported files and concatenate them into a single output file.
    """
    supported_files = get_all_supported_files(PROJECT_ROOT)
    # Optionally sort the files for dependency handling
    supported_files.sort()
    concatenate_files(supported_files, OUTPUT_FILE)

if __name__ == '__main__':
    main()

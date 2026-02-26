#!/usr/bin/env python3
"""
Script to extract all Python code files from the AI_ModelEval project
into a single text file with file path headers.
"""

import os
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent  # Assumes script is in project root
OUTPUT_FILE = PROJECT_ROOT / "code_extract.txt"
EXCLUDE_DIRS = {
    '.venv', 'venv', 'env', '.git', '__pycache__', 
    'node_modules', '.pytest_cache', '.mypy_cache',
    'dist', 'build', '*.egg-info', '.next'
}
EXCLUDE_FILES = {
    'extract_code.py',  # Exclude this script itself
    'code_extract.txt'  # Exclude previous extracts
}
FILE_EXTENSIONS = {'.py', '.yaml', '.yml', '.json', '.md', '.txt', '.cfg', '.ini', '.ts' , '.tsx', '.js', '.jsx'}

def should_include_file(file_path: Path) -> bool:
    """Check if file should be included in extraction"""
    # Check if file is in excluded directory
    for part in file_path.parts:
        if part in EXCLUDE_DIRS or any(pattern in part for pattern in EXCLUDE_DIRS):
            return False
    
    # Check if file is excluded by name
    if file_path.name in EXCLUDE_FILES:
        return False
    
    # Check file extension
    if file_path.suffix.lower() in FILE_EXTENSIONS:
        return True
    
    return False

def extract_files():
    """Extract all code files into a single text file"""
    print(f"Extracting code from {PROJECT_ROOT}")
    print(f"Output will be saved to: {OUTPUT_FILE}")
    
    # Collect all files
    files_to_extract = []
    for file_path in PROJECT_ROOT.rglob('*'):
        if file_path.is_file() and should_include_file(file_path):
            files_to_extract.append(file_path)
    
    # Sort files for consistent output
    files_to_extract.sort()
    
    print(f"Found {len(files_to_extract)} files to extract")
    
    # Write to output file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        # Write header
        out_f.write("=" * 80 + "\n")
        out_f.write("AI_ModelEval CODE EXTRACTION\n")
        out_f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_f.write(f"Total files: {len(files_to_extract)}\n")
        out_f.write("=" * 80 + "\n\n")
        
        # Write each file
        for i, file_path in enumerate(files_to_extract, 1):
            relative_path = file_path.relative_to(PROJECT_ROOT)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as in_f:
                    content = in_f.read()
                
                # Write file header
                out_f.write("-" * 80 + "\n")
                out_f.write(f"FILE {i}/{len(files_to_extract)}: {relative_path}\n")
                out_f.write("-" * 80 + "\n\n")
                
                # Write file content
                out_f.write(content)
                
                # Add newlines between files
                if not content.endswith('\n'):
                    out_f.write('\n')
                out_f.write('\n')
                
                print(f"  Extracted: {relative_path}")
                
            except UnicodeDecodeError:
                print(f"  Skipping binary file: {relative_path}")
                out_f.write(f"[BINARY FILE - CONTENT NOT DISPLAYED]\n\n")
            except Exception as e:
                print(f"  Error reading {relative_path}: {e}")
                out_f.write(f"[ERROR READING FILE: {e}]\n\n")
    
    print(f"\nExtraction complete! Output saved to: {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE) / 1024:.2f} KB")

def main():
    """Main function"""
    print("=" * 60)
    print("AI_ModelEval Code Extractor")
    print("=" * 60)
    
    # Confirm with user
    response = input(f"This will extract all code files to {OUTPUT_FILE}. Continue? (y/n): ")
    if response.lower() == 'y':
        extract_files()
    else:
        print("Extraction cancelled.")

if __name__ == "__main__":
    main()
import os
from pathlib import Path

def extract_codes_to_single_file(source_dir=".", output_file="all_codes.txt", excluded_folders=['venv']):
    """
    Extract all code files content into a single text file,
    excluding specified folders.
    
    Args:
        source_dir (str): Source directory to search for code files
        output_file (str): Output text file name
        excluded_folders (list): List of folder names to exclude
    """
    
    # Common code file extensions
    code_extensions = {
        '.py', '.java', '.cpp', '.c', '.h', '.hpp', '.js', '.ts', '.jsx', '.tsx',
        '.html', '.css', '.scss', '.php', '.rb', '.go', '.rs', '.swift', '.kt',
        '.sql', '.sh', '.bash', '.r', '.m', '.mat', '.scala', '.pl', '.pm',
        '.lua', '.tcl', '.xml', '.json', '.yaml', '.yml', '.md', '.txt',
        '.cs', '.fs', '.vb', '.asm', '.s', '.f', '.for', '.f90', '.f95'
    }
    
    code_files_found = []
    total_files = 0
    
    print(f"Extracting code files from: {source_dir}")
    print(f"Excluding folders: {excluded_folders}")
    print(f"Output file: {output_file}")
    print("-" * 60)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header
        outfile.write("=" * 80 + "\n")
        outfile.write("EXTRACTED CODE FILES\n")
        outfile.write(f"Source Directory: {source_dir}\n")
        outfile.write(f"Excluded Folders: {excluded_folders}\n")
        outfile.write("=" * 80 + "\n\n")
        
        for root, dirs, files in os.walk(source_dir):
            # Remove excluded folders from dirs to prevent walking into them
            dirs[:] = [d for d in dirs if d not in excluded_folders]
            
            for file in files:
                file_path = Path(root) / file
                file_extension = file_path.suffix.lower()
                
                # Check if file has a code extension
                if file_extension in code_extensions:
                    try:
                        relative_path = file_path.relative_to(source_dir)
                        code_files_found.append(relative_path)
                        
                        # Write file header
                        outfile.write("\n" + "=" * 80 + "\n")
                        outfile.write(f"FILE: {relative_path}\n")
                        outfile.write(f"PATH: {file_path}\n")
                        outfile.write("=" * 80 + "\n\n")
                        
                        # Read and write file content
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(content)
                            outfile.write("\n")  # Add newline at end of file
                        
                        print(f"✓ Added: {relative_path}")
                        total_files += 1
                        
                    except UnicodeDecodeError:
                        print(f"✗ Skipped (encoding issue): {relative_path}")
                    except Exception as e:
                        print(f"✗ Error reading {relative_path}: {e}")
        
        # Write summary
        outfile.write("\n" + "=" * 80 + "\n")
        outfile.write("SUMMARY\n")
        outfile.write(f"Total files extracted: {total_files}\n")
        outfile.write("=" * 80 + "\n")
    
    return code_files_found, total_files

def main():
    # Configuration
    source_directory = input("Enter source directory path (default: current directory): ").strip()
    if not source_directory:
        source_directory = "."
    
    output_filename = input("Enter output filename (default: 'all_codes.txt'): ").strip()
    if not output_filename:
        output_filename = "all_codes.txt"
    
    # Additional excluded folders (optional)
    additional_excluded = input("Enter additional folders to exclude (comma-separated, or press enter for none): ").strip()
    excluded_folders = ['venv']
    
    if additional_excluded:
        excluded_folders.extend([folder.strip() for folder in additional_excluded.split(',')])
    
    print(f"\nStarting extraction...")
    print(f"Source: {source_directory}")
    print(f"Output: {output_filename}")
    print(f"Excluded folders: {excluded_folders}")
    print("-" * 60)
    
    try:
        # Extract code files to single file
        code_files, total_files = extract_codes_to_single_file(
            source_directory, output_filename, excluded_folders
        )
        
        print("-" * 60)
        print(f"Extraction completed!")
        print(f"Total code files extracted: {total_files}")
        print(f"Output file: {output_filename}")
        
        # Display file types summary
        file_types = {}
        for file_path in code_files:
            ext = Path(file_path).suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        print("\nFile type summary:")
        for ext, count in sorted(file_types.items()):
            print(f"  {ext}: {count} files")
            
    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    main()
"""
Utility script for exporting the project source into a single text file.

Traverses the project directory, filters files by extension, and writes
their contents into a consolidated output file for sharing or inspection.
"""
import os

# ==============================
# CONFIG CONSTANTS
# ==============================
OUTPUT_FILE = "project_dump.txt"

# Extensions to include
INCLUDE_EXTENSIONS = {".py", ".json", ".txt", ".md", ".yaml", ".yml"}

# Folders to skip
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build"
}

# ==============================
# FUNCTIONS
# ==============================
def should_include_file(filename: str) -> bool:
    """
    Determine whether a file should be included based on its extension.

    Args:
        filename: The name of the file to evaluate.

    Returns:
        True if the file's extension is allowed, otherwise False.
    """    
    return os.path.splitext(filename)[1].lower() in INCLUDE_EXTENSIONS

def collect_files(root_dir: str) -> list[str]:
    """
    Recursively collect all files under the given directory that match
    the allowed extensions, excluding specified folders.

    Args:
        root_dir: The root directory to search.

    Returns:
        A sorted list of file paths to include.
    """    
    files: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to skip excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for filename in filenames:
            if should_include_file(filename):
                full_path = os.path.join(dirpath, filename)
                files.append(full_path)

    return sorted(files)

def write_output(files: list[str], root_dir: str) -> None:
    """
    Write the contents of collected files into a single output file.

    Each file is prefixed with its relative path for clarity. Files that
    cannot be read are noted in the output.

    Args:
        files: The list of file paths to include.
        root_dir: The root directory used to compute relative paths.
    """
    try:        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            for path in files:
                rel_path = os.path.relpath(path, root_dir)

                out.write("=" * 80 + "\n")
                out.write(f"FILE: {rel_path}\n")
                out.write("=" * 80 + "\n\n")

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        out.write(f.read())
                except OSError as e:
                    out.write(f"[ERROR READING FILE: {e}]")

                out.write("\n\n\n")
    except OSError as e:
        print(f"ERROR: Could not write output file '{OUTPUT_FILE}': {e}")                    

if __name__ == "__main__":
    root = os.getcwd()
    files = collect_files(root)
    write_output(files, root)

    print(f"Done. Output written to {OUTPUT_FILE}")
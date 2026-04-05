import os

OUTPUT_FILE = "project_dump.txt"

# Extensions you want to include
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

def should_include_file(filename: str) -> bool:
    return os.path.splitext(filename)[1].lower() in INCLUDE_EXTENSIONS

def collect_files(root_dir: str) -> list[str]:
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

if __name__ == "__main__":
    root = os.getcwd()
    files = collect_files(root)
    write_output(files, root)

    print(f"Done. Output written to {OUTPUT_FILE}")
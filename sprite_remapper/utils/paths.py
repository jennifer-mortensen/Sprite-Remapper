"""
Path utilities and shared filesystem locations for sprite_remapper.

Provides helpers for resolving application directories, normalizing
filenames, and defining commonly used project file paths.
"""
from pathlib import Path
import sys

# ==============================
# PATH HELPERS
# ==============================
def get_base_dir() -> Path:
    """
    Return the application's root directory.

    When running as a packaged executable (such as PyInstaller),
    this resolves to the executable's parent folder.

    When running from source, this resolves to the project root
    based on this module's location.

    Returns:
        The root directory as a Path object.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent

def normalize_filename(filename: str, extension: str) -> Path:
    """
    Ensure a filename includes the specified extension.

    Args:
        filename: The filename to normalize.
        extension: The required file extension.

    Returns:
        A Path object with the correct extension.
    """    
    path = Path(filename)
    return path if path.suffix else path.with_suffix(f".{extension}")

# ==============================
# PATHS CONSTANTS
# ==============================
# Directories
PROJECT_ROOT = get_base_dir()
FILE_DIR_PALETTES = PROJECT_ROOT / "palettes"

# Files
FILE_PATH_CONFIG = PROJECT_ROOT / normalize_filename("config", "json")
FILE_PATH_LOG = PROJECT_ROOT / normalize_filename("sprite_remapper", "log")

# File extensions
FILE_EXTENSION_PALETTE = "json"
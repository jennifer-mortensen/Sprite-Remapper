"""
Shared application constants for sprite_remapper.

Defines reusable static values such as encodings, logging settings,
default modes, and other configuration values used across modules.
"""
# ==============================
# FILE ENCODING
# ==============================
DEFAULT_ENCODING = "utf-8"

# ==============================
# LOGGER CONSTANTS
# ==============================
LOGGER_FORMAT_CLI = "%(levelname)s: %(message)s"
LOGGER_FORMAT_FILE = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOGGER_FILE_MODE = "w" # "w" = overwrite each run
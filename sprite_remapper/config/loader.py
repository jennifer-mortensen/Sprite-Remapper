"""
Configuration loading utilities for sprite_remapper.

Provides functionality for reading, validating, and converting external
configuration files into structured application data.
"""
import logging
import json
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ==============================
# DATA CLASSES
# ==============================
@dataclass
class Config:
    palette: str
    input: str
    output: str
    tile_width: int
    tile_height: int
    color_space: str = "rgb"

# ==============================
# HIGH LEVEL FUNCTIONS
# ==============================
def load_config(path: Path) -> Config:
    """
    Load and parse a configuration file into a Config object.

    Reads JSON data from the given path, filters out unknown keys,
    and constructs a Config instance using the recognized fields.

    Args:
        path: The path to the configuration file.

    Returns:
        A populated Config object.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        TypeError: If required fields are missing or have invalid types.
    """    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    allowed_keys = Config.__annotations__.keys()

    unknown_keys = set(data) - set(allowed_keys)
    if unknown_keys:
        logger.warning(f"Unknown config keys: {unknown_keys}")

    filtered = {key: value for key, value in data.items() if key in allowed_keys}

    return Config(**filtered)
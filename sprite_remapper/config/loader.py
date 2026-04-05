import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    palette: str
    input: str
    output: str
    tile_width: int
    tile_height: int
    color_space: str = "rgb"

def load_config(path: Path) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    allowed_keys = Config.__annotations__.keys()

    unknown_keys = set(data) - set(allowed_keys)
    if unknown_keys:
        print(f"[WARNING] Unknown config keys: {unknown_keys}")

    filtered = {k: v for k, v in data.items() if k in allowed_keys}

    return Config(**filtered)
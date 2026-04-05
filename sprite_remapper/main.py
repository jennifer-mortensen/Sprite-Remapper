from pathlib import Path
from sprite_remapper.core.pipeline import run_pipeline
from sprite_remapper.config.loader import load_config, Config
from typing import Any
import json

def main() -> None:
    base_dir = Path(__file__).resolve().parent

    config_path = base_dir / "config.json"
    config: Config = load_config(config_path)

    palette_path = base_dir / resolve_palette_path(config.palette)

    with open(palette_path, "r", encoding="utf-8") as f:
        palette: dict[str, Any] = json.load(f)

    run_pipeline(
        input_path=base_dir / config.input,
        output_path=base_dir / config.output,
        tile_width=config.tile_width,
        tile_height=config.tile_height,
        palette=palette,
        color_space=config.color_space
    )

def resolve_palette_path(name: str) -> Path:
    path = Path(name)

    if path.suffix:
        return path

    return Path("palettes") / f"{name}.json"

if __name__ == "__main__":
    main()
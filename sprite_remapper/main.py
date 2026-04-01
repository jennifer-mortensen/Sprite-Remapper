
from pathlib import Path
from sprite_remapper.core.pipeline import run_pipeline
from sprite_remapper.config.loader import load_config

def main():
    base_dir = Path(__file__).resolve().parent  # package root

    config_path = base_dir / "config.json"
    config = load_config(config_path)

    palette_path = base_dir / "palettes" / f"{config['palette']}.json"
    palette = load_config(palette_path)

    run_pipeline(
        input_path=base_dir / config["input"],
        output_path=base_dir / config["output"],
        tile_width=config["tile_width"],
        tile_height=config["tile_height"],
        palette=palette,
        color_space=config.get("color_space", "rgb")
    )

def resolve_palette_path(name):
    path = Path(name)

    # If it's already a path (user provided full path)
    if path.suffix:
        return path

    # Otherwise assume palettes/<name>.json
    return Path("palettes") / f"{name}.json"    

if __name__ == "__main__":
    main()
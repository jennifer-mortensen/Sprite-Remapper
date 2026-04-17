"""
Application entry point for sprite_remapper.

Handles startup concerns such as logging, configuration loading,
resource path resolution, and launching the processing pipeline.
"""
from sprite_remapper.config.loader import load_config, Config
from sprite_remapper import const
from sprite_remapper.core.pipeline import run_pipeline
from sprite_remapper.utils import paths
from typing import Any
import json
import logging
import sys

logger = logging.getLogger(__name__)

# ==============================
# MAIN ENTRY POINT
# ==============================
def main() -> None:
    """
    Run the sprite remapping application.

    Initializes logging, loads configuration data, resolves the
    selected palette, and executes the image processing pipeline.

    If an unrecoverable error occurs, the exception is logged,
    a user-friendly message is displayed, and the program exits
    with a non-zero status code.
    """    
    configure_logging()
    
    try:
        # Load config and prepare paths
        config: Config = load_config(paths.FILE_PATH_CONFIG)        
        palette_path = paths.FILE_DIR_PALETTES / paths.normalize_filename(config.palette, paths.FILE_EXTENSION_PALETTE)

        # Open the palette file
        with open(palette_path, "r", encoding=const.DEFAULT_ENCODING) as f:
            palette: dict[str, Any] = json.load(f)

        # Process the sprite file
        run_pipeline(
            input_path=paths.PROJECT_ROOT / config.input,
            output_path=paths.PROJECT_ROOT / config.output,
            tile_width=config.tile_width,
            tile_height=config.tile_height,
            palette=palette,
            color_space=config.color_space
        )
    except Exception:
        logger.exception("Unexpected error")
        # Separate CLI-level output. Full exception is logged externally just above.
        print(
            f"ERROR: An unexpected error occurred. "
            f"See the log file (default: {paths.FILE_PATH_LOG}) for details."
        )
        sys.exit(1)

# ==============================
# HIGH LEVEL FUNCTIONS
# ==============================
def configure_logging() -> None:
    """
    Configure logging for both CLI and file output.

    CLI logging displays human-readable messages, while file logging
    includes debug information and full exception tracebacks.
    """    
    formatter = logging.Formatter(const.LOGGER_FORMAT_FILE)

    # CLI-level logging. Prioritize readability.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(const.LOGGER_FORMAT_CLI))

    # Filter out exception tracebacks from CLI
    class NoExceptionTracebackFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            return record.exc_info is None

    console.addFilter(NoExceptionTracebackFilter())

    # File-level logging. Full fidelity.
    file_handler = logging.FileHandler(
        paths.FILE_PATH_LOG,
        mode=const.LOGGER_FILE_MODE,
        encoding=const.DEFAULT_ENCODING
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers = [console, file_handler]

if __name__ == "__main__":
    main()
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

PROJ_ROOT = Path(__file__).resolve().parents[1]


def _format_message(record):
    # process record to generate
    t = record["time"]
    level = record["level"]

    file = record["file"]
    function = record["function"]
    line = record["line"]

    message = record["message"]

    # escape tags in message, tags are "<some_tag>"
    if function.startswith("<") and function.endswith(">"):
        function = rf"\{function}"

    message.replace("<", r"\<")

    # strip the path to the project root and replace it with a dot for brevity in both file and message
    file = str(file.path).replace(str(PROJ_ROOT), "$PROJECT_ROOT")
    message = message.replace(str(PROJ_ROOT), "$PROJECT_ROOT")

    return (
        f"<green>{t:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        f"<level>{level: <8}</level> | "
        f"<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n"
    )


logger.remove(0)

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.add(lambda msg: tqdm.write(msg, end=""), format=_format_message, colorize=True)
except ModuleNotFoundError:
    logger.add(sys.stderr, format=_format_message, colorize=True)

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass

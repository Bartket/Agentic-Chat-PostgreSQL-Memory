import logging
import os

from starlette.config import Config
from pydantic.types import SecretStr

config = Config(".env") if os.path.exists(".env") else Config()

# OpenAI settings
GEMINI_API_KEY = config("GEMINI_API_KEY", cast=SecretStr, default=None)
MODEL_NAME = config("MODEL_NAME", cast=str, default="gemini-2.5-flash")

# DB settings
CHECKPOINT_URL = config(
    "CHECKPOINT_URL",
    cast=str,
    default="postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable",
)


# Init Logger
def init_logger() -> logging.Logger:
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)
    return logger


logger = init_logger()

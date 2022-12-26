from dotenv import load_dotenv

from pathlib import Path

DEFAULT_ENV_PATH = Path().home() / ".bux-token.env"

def read_env_file(*, file_path: str | Path = DEFAULT_ENV_PATH) -> None:
    """
    Get the token either in file or environment variables
    """
    if not Path(file_path).exists():
        raise Exception(
            f"No environment file found in default or provided path: {file_path}"
        )

    is_loaded = load_dotenv(file_path)

    if not is_loaded:
        raise Exception(f"File for configuration is empty: {file_path}")
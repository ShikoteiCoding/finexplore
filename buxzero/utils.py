from dotenv import load_dotenv

from pathlib import Path

DEFAULT_ENV_PATH = Path().home() / ".bux-token.env"


def printable_banner(text: str, length: int = 50) -> str:
    """Print a beautified banner."""
    assert type(length) == int, "Please length should be an int."

    if len(text) > length:
        length = len(text) + 10

    odd = (length - len(text)) % 2

    border = "#" * (((length - len(text)) // 2) + odd - 1)

    output = (
        "\n"
        + "#" * (length + odd)
        + "\n"
        + border
        + " "
        + text
        + " "
        + border
        + "\n"
        + "#" * (length + odd)
    )
    return output


def read_environment_file(*, file_path: str | Path = DEFAULT_ENV_PATH) -> None:
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

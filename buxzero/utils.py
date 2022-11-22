from dotenv import load_dotenv

def printable_banner(text:str, length:int=50) -> str:
    """ Print a beautified banner. """
    assert type(length) == int, "Please length should be an int."

    if len(text) > length:
        length = len(text) + 10
    
    odd = (length - len(text)) % 2

    border = "#" * (((length - len(text)) // 2) + odd - 1)

    output = "\n" + "#" * (length + odd) + "\n" + border + " " + text + " " + border + "\n" + "#" * (length + odd)
    return output


def read_environment_file(env_path="token.env") -> None:
    """
    Get the token either in file or environment variables
    """
    try:
        load_dotenv("token.env")
    except Exception as e:
        print(f"No environment file found: {e}")

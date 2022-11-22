from dotenv import load_dotenv


def read_environment_file(env_path="token.env") -> None:
    """
    Get the token either in file or environment variables
    """
    try:
        load_dotenv("token.env")
    except Exception as e:
        print(f"No environment file found: {e}")

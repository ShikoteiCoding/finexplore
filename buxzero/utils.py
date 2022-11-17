from dotenv import load_dotenv
from _user import GuestAPI

def read_environment_file(env_path="token.env") -> None:
    """
    Get the token either in file or environment variables
    """
    try:
        load_dotenv("token.env")
    except Exception as e:
        print(f"No environment file found: {e}")

def create_token_command() -> None:
    """
    Logic to require token necessities to user.
    """
    email = input("1. Enter email: ")
    api = GuestAPI()
    api.request_link(email).requests()
    print("2. Check your mailbox.")
    magic_link = input("3. Enter magic link: ")
    token = api.get_token(magic_link).requests()
    print(token)
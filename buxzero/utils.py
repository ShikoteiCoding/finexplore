from dotenv import load_dotenv
from _user import GuestAPI

def get_or_create_token(env_path="token.env") -> None:
    """
    Get the token either in file or environment variables
    """
    try:
        load_dotenv("token.env")
    except Exception as e:
        print(f"No environment file found: {e}")
        create_token_command()
        print("Please create an environment file with the variable BUX_TOKEN.")

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
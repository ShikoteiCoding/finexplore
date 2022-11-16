import os

from _user import GuestAPI
from dotenv import load_dotenv

def get_token(env_path="token.env") -> str:
    """
    Get the token either in file or environment variables
    """
    try:
        load_dotenv("token.env")
    except Exception as e:
        print(f"No environment file found: {e}")
    token = os.getenv("BUX_TOKEN")
    if not token:
        return get_token_command()

    return token

def get_token_command() -> str:
    """
    Logic to require token necessities to user.
    """
    email = input('1. Enter email: ')
    api = GuestAPI()
    api.request_link(email).requests()
    print('2. Check your mailbox.')
    magic_link = input('3. Enter magic link: ')
    token = api.get_token(magic_link).requests()
    return token
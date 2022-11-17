from _user import GuestAPI

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
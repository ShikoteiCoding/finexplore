from user import GuestAPI

from ._commands import Command, register


@register
class GetToken(Command):
    """
    Enquire necessities from customer to get the API token from buxzero magic-link.
    """

    name: str = "get-token"

    def run(self) -> int:
        email = input("1. Enter email: ")
        api = GuestAPI()
        api.request_link(email).requests()
        print("2. Check your mailbox.")
        magic_link = input("3. Enter magic link: ")
        token = api.get_token(magic_link).requests()
        print(token)
        return 0

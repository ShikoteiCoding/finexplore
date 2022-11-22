from ._response import Response


class Me(Response):
    """
    Me endpoint of bux. Get general account data.
    """

    @property
    def account_type(self) -> str:
        return self["accountType"]

    @property
    def account_status(self) -> str:
        return self["accountStatus"]

    @property
    def pin_status(self) -> str:
        return self["pinStatus"]

    @property
    def user_id(self) -> str:
        return self["profile"]["userId"]

    @property
    def nickname(self) -> str:
        return self["profile"]["nickname"] or ""  # Replace None by empty

from .response import Response

from datetime import datetime


class Message(Response):
    """
    Message from Inbox endpoint of bux. Get message about dividends and past moves.
    """

    @property
    def id(self) -> str:
        return self["id"]

    @property
    def time(self) -> datetime:
        return datetime.fromtimestamp(self["timestamp"] / 1000)

    @property
    def type(self) -> str:
        return self["type"]

    @property
    def unread(self) -> bool:
        return self["unread"]

    @property
    def icon(self) -> str:
        return self["content"]["icon"]

    @property
    def image(self) -> str | None:
        return self["content"].get("image")

    @property
    def link(self) -> str | None:
        return self["content"].get("link")

    @property
    def title(self) -> str:
        return self["content"]["title"]

    @property
    def description(self) -> str:
        return self["content"]["subtitle"]

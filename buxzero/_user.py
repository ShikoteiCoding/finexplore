from dataclasses import dataclass
from typing import NamedTuple

from _config import Config
from _request import Request

from . import types


@dataclass
class UserAPI(NamedTuple):
    token: str
    config: Config

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "authorization": f"Bearer {self.token}",
            "pin-authorization": "Bearer null",
            **self.config.headers,
        }

    def me(self) -> Request[types.Me]:
        return Request(
            url=f"{self.config.stocks_url}/portfolio-query/13/users/me",
            headers=self._headers,
            on_json=types.Me,
        )

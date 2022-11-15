from dataclasses import dataclass
from typing import NamedTuple

import responses
from _config import Config
from _request import Request


class UserAPI(NamedTuple):
    token: str
    config: Config = Config()

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "authorization": f"Bearer {self.token}",
            "pin-authorization": "Bearer null",
            **self.config.headers,
        }

    def me(self) -> Request[responses.Me]:
        return Request(
            url=f"{self.config.stocks_url}/portfolio-query/13/users/me",
            headers=self._headers,
            on_json=responses.Me,
        )

from dataclasses import dataclass, field


import responses
from config import Config
from _request import Request


@dataclass
class UserAPI:
    config: Config = field(default_factory=Config)

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "authorization": f"Bearer {self.config.token}",
            "pin-authorization": "Bearer null",
            **self.config.headers,
        }

    def me(self) -> Request[responses.Me]:
        return Request(
            url=f"{self.config.stocks_url}/portfolio-query/13/users/me",
            headers=self._headers,
            on_json=responses.Me,
        )

    def portfolio(self) -> Request[responses.Portfolio]:
        return Request(
            url=f'{self.config.stocks_url}/portfolio-query/13/users/me/portfolio',
            headers=self._headers,
            on_json=responses.Portfolio,
        )

    def personal_data(self) -> Request[responses.PersonalData]:
        return Request(
            url=f'{self.config.stocks_url}/personal-data-service/13/user',
            headers=self._headers,
            on_json=responses.PersonalData,
        )

@dataclass
class GuestAPI:
    config: Config = field(default_factory=Config)

    def request_link(self, email: str) -> Request[bool]:
        return Request(
            method="POST",
            url=f"{self.config.auth_url}/magic-link",
            headers={
                "authorization": "Basic ODQ3MzYyMzAxMDpaTUhaM1RZT1pIVUxFRlhMUDRRQ1BIV0k1RDNWQVpNNw==",
                **self.config.headers,
            },
            data={"email": email},
            on_status=lambda status: status == 202,
        )

    def get_token(self, magic_link: str) -> Request[str]:
        magic_link = magic_link.split("/")[-1]
        return Request(
            method="POST",
            url=f"{self.config.auth_url}/authorize",
            headers={
                "authorization": "Basic ODQ3MzYyMzAxMzpHRFNTS1ozUU5RQ081QkNXN0RJRFhVWEE2RENSUUNNRQ==",
                **self.config.headers,
            },
            data={
                "credentials": {"token": magic_link},
                "type": "magiclink",
            },
            on_json=lambda data: data["access_token"],
        )

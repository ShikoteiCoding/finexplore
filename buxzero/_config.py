from typing import NamedTuple, Mapping
from types import MappingProxyType


class Config(NamedTuple):
    auth_url: str = "https://auth.getbux.com/api/3"
    stocks_url: str = "https://stocks.prod.getbux.com"
    ws_url: str = "wss://stocks.prod.getbux.com/rtf/1/subscriptions/me"
    headers: Mapping = MappingProxyType(
        {
            "accept-language": "en",
            "x-app-version": "4.7-7174",
            "x-os-version": "9",
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/4.9.1",
        }
    )

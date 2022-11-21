from dataclasses import KW_ONLY, dataclass, field
from http import HTTPStatus
from typing import Mapping, Generic, TypeVar, Any, Callable

import requests

T = TypeVar("T")


class HTTPError(Exception):
    status: HTTPStatus
    text: str

    def __init__(self, status: int, text: str) -> None:
        self.status = HTTPStatus(status)
        self.text = text


@dataclass
class Request(Generic[T]):
    _: KW_ONLY

    url: str
    headers: Mapping
    method: str = field(default="GET")

    body: None | bytes = field(default=None)
    data: None | dict[str, Any] = field(default=None)
    params: None | dict[str, Any] = field(default=None)
    on_json: None | Callable[[Any], T] = field(default=None)
    on_status: None | Callable[[int], T] = field(default=None)

    
    def requests(self) -> T:
        response = requests.request(
            method=self.method,
            url=self.url,
            data=self.body,
            json=self.data,
            params=self.params,
            headers=self.headers,
        )
        if response.status_code >= 300:
            raise HTTPError(response.status_code, response.text)
        if self.on_json:
            return self.on_json(response.json())
        if self.on_status:
            return self.on_status(response.status_code)
        return response.json()

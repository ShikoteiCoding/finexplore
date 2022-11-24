import os
import pytest

from types import MappingProxyType

import bux.config as config


AUTH_URL = "https://auth.getbux.com/api/3"
STOCKS_URL = "https://stocks.prod.getbux.com"
WS_URL = "wss://stocks.prod.getbux.com/rtf/1/subscriptions/me"

BUX_TOKEN = "ABCD"

def test_load() -> None:
    c = config.load_config()

    assert type(c) == config.Config
    assert c.auth_url == AUTH_URL
    assert c.stocks_url == STOCKS_URL
    assert c.ws_url == WS_URL
    assert type(c.headers) == MappingProxyType
    assert c.token == ""

def test_token_opts_is_correct() -> None:
    os.environ["BUX_TOKEN"] = BUX_TOKEN
    c = config.load_config(config.load_token_opts)
    assert c.token == BUX_TOKEN

def test_token_opts_is_not_correct() -> None:
    # Verify not proper variable
    os.environ["BUX_TOKEN"] = "ABC"
    c = config.load_config(config.load_token_opts)
    assert c.token != BUX_TOKEN

def test_token_opts_raise_error() -> None:
    # Verify raised error if no variable
    os.environ["BUX_TOKEN"] = ""
    with pytest.raises(config.MissingVariableException) as _:
        config.load_config(config.load_token_opts)

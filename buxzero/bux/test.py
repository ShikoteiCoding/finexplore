import unittest

import os
from types import MappingProxyType

from config import (
    Config,
    load_config as load,
    load_token_opts,
    MissingVariableException,
)


AUTH_URL = "https://auth.getbux.com/api/3"
STOCKS_URL = "https://stocks.prod.getbux.com"
WS_URL = "wss://stocks.prod.getbux.com/rtf/1/subscriptions/me"

BUX_TOKEN = "ABCD"


class Testconfig(unittest.TestCase):
    def test_load(self) -> None:
        c = load()

        self.assertEqual(type(c), Config)
        self.assertEqual(c.auth_url, AUTH_URL)
        self.assertEqual(c.stocks_url, STOCKS_URL)
        self.assertEqual(c.ws_url, WS_URL)
        self.assertEqual(type(c.headers), MappingProxyType)
        self.assertEqual(c.token, "")

    def test_token_opts(self) -> None:
        # Verify proper variable
        os.environ["BUX_TOKEN"] = BUX_TOKEN
        c = load(load_token_opts)
        self.assertEqual(c.token, BUX_TOKEN)

        # Verify not proper variable
        os.environ["BUX_TOKEN"] = "ABC"
        c = load(load_token_opts)
        self.assertNotEqual(c.token, BUX_TOKEN)

        # Verify raised error if no variable
        os.environ["BUX_TOKEN"] = ""
        self.assertRaises(MissingVariableException, load, load_token_opts)


class TestResponseMe(unittest.TestCase):
    ...


if __name__ == "__main__":
    unittest.main()

import unittest
import sys
from dotenv import load_dotenv
from .helpers import check_properties

sys.path.append("..")
import bux
from bux.config import load_config, load_token_opts

class TestMe(unittest.TestCase):
    def setUp(self):
        load_dotenv("token.env")
        c = load_config(load_token_opts)
        self.api = bux.UserAPI(config=c)

    def test_me(self):
        check_properties(
            self.api.me.requests(),
            []
        )

class TestPersonalData(unittest.TestCase):
    def test_personal_data(self):
        ...

class TestPortfolio(unittest.TestCase):
    def test_portfolio(self):
        ...

# import sys
import pytest
from dotenv import load_dotenv

# sys.path.append("..")
import bux


@pytest.fixture
def config() -> bux.Config:
    load_dotenv("token.env")
    return bux.config.load_config(bux.config.load_token_opts)


@pytest.fixture
def api(config: bux.Config) -> bux.UserAPI:
    return bux.UserAPI(config=config)

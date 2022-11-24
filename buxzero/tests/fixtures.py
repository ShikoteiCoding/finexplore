import sys
import pytest
from dotenv import load_dotenv

sys.path.append("..")
import bux

@pytest.fixture
def api(config: bux.Config) -> bux.UserAPI:
    return bux.UserAPI(config=config)
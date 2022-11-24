import pytest

import bux
from .helpers import check_has_properties
from .fixtures import api, config


def test_me(api: bux.UserAPI) -> None:
    me = api.me.requests()

    assert me.account_status == 'READY'
    assert me.account_type == 'USER'
    assert me.pin_status == 'ENABLED'

    check_has_properties(
        me,
        [ "account_type", "account_status", "pin_status", "user_id", "nickname"]
    )
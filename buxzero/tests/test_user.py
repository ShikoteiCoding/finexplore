import pytest

import bux
from .helpers import assert_fields_have_getters
from .fixtures import api, config


def test_me(api: bux.UserAPI) -> None:
    response = api.me.requests()
    fields = {
        'accountStatus',
        'usMarketDataSubscriptionActivated',
        'pinStatus',
        'communicationConfiguration',
        'profile',
        'etfAgreementAccepted',
        'accountType',
        'reassessmentInfo',
    }
    assert set(response) == fields

    assert response.account_status == 'READY'
    assert response.account_type == 'USER'
    assert response.pin_status == 'ENABLED'

    assert_fields_have_getters(
        response, 
        exclude={"usMarketDataSubscriptionActivated", "etfAgreementAccepted", "communicationConfiguration", "reassessmentInfo", "nickname"},
        unwrap={"profile"}
    )
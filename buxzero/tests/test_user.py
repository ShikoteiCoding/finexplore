import pytest

import bux
from .helpers import assert_fields_exist, assert_fields_have_getters
from .fixtures import api, config


def test_me(api: bux.UserAPI) -> None:
    response = api.me.requests()
    fields = {
        "accountStatus",
        "accountType",
        "communicationConfiguration.monthlyTransactionsReportingEnabled",
        "etfAgreementAccepted",
        "pinStatus",
        "profile.nickname",
        "profile.userId",
        "reassessmentInfo.required",
        "usMarketDataSubscriptionActivated",
    }
    assert_fields_exist(response, fields)

    assert response.account_status == "READY", "The provided account is not ready to use."
    assert response.account_type == "USER"
    assert response.pin_status == "ENABLED"

    assert_fields_have_getters(
        response, 
        exclude={
            "usMarketDataSubscriptionActivated", 
            "etfAgreementAccepted", 
            "communicationConfiguration.monthlyTransactionsReportingEnabled", 
            "reassessmentInfo.required", 
            "profile.nickname"
        }
    )
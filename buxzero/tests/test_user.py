import pytest

import bux
from .helpers import assert_fields_exist, assert_fields_have_getters
from .fixtures import api, config


def test_me(api: bux.UserAPI) -> None:
    response = api.me.requests()
    fields = {
        "accountStatus",
        "accountType",
        "communicationConfiguration",
        "etfAgreementAccepted",
        "pinStatus",
        "profile.nickname",
        "profile.userId",
        "reassessmentInfo",
        "usMarketDataSubscriptionActivated",
    }
    assert_fields_exist(response, fields)

    assert (
        response.account_status == "READY"
    ), "The provided account is not ready to use."
    assert response.account_type == "USER"
    assert response.pin_status == "ENABLED"

    assert_fields_have_getters(
        response,
        exclude={
            "usMarketDataSubscriptionActivated",
            "etfAgreementAccepted",
            "communicationConfiguration.monthlyTransactionsReportingEnabled",
            "reassessmentInfo.required",
            "profile.nickname",
        },
    )


def test_personal_data(api: bux.UserAPI) -> None:
    response = api.personal_data.requests()

    fields = {"countryOfResidence", "email", "firstName", "lastName", "tobExempted"}
    assert_fields_exist(response, fields)

    assert_fields_have_getters(response, exclude={"countryOfResidence", "tobExempted"})

def test_portfolio(api: bux.UserAPI) -> None:
    response = api.portfolio.requests()

    fields = {
        'accountValue',
        'allTimeDepositAndWithdraws',
        'allTimeTradesAmount',
        'availableCash',
        'cashBalance',
        'intraDayTradesAmount',
        'investedAmount',
        'marketsOpen',
        'orders',
        'positions',
        'previousClosingAmount',
        'reservedCash',
    }
    assert_fields_exist(response, fields)
    
    #assert_fields_have_getters(response, exclude={"countryOfResidence", "tobExempted"})
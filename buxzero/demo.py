from config import load_config as load, load_token_opts

from _user import UserAPI

from decimal import Decimal
import utils
import pandas as pd

if __name__ == "__main__":

    utils.read_environment_file()

    c = load(load_token_opts)

    api = UserAPI(config=c)

    # me = api.me.requests()
    # pd = api.personal_data.requests()
    portfolio = api.portfolio.requests()

    positions = portfolio.positions

    df = positions.to_pandas()
    df["total"] = df.apply(lambda x: Decimal(x["quantity"]) * x["offer.amount"], axis=1)

    base_currency_sum = df["total"].sum()
    print(base_currency_sum, type(base_currency_sum))

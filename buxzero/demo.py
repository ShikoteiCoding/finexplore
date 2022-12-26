from bux.config import load_config as load, load_token_opts

from bux import UserAPI

from decimal import Decimal

import utils as utils
import pandas as pd

from pprint import PrettyPrinter

if __name__ == "__main__":

    utils.read_environment_file()

    pp = PrettyPrinter(indent=2)

    c = load(load_token_opts)

    api = UserAPI(config=c)

    print(utils.printable_banner('"Me" Endpoint'))
    me = api.me.requests()
    pp.pprint(dict(me))

    print(utils.printable_banner('"Personal Data" Endpoint'))
    pdata = api.personal_data.requests()
    pp.pprint(dict(pdata))

    print(utils.printable_banner('"Portfolio" Endpoint'))
    portfolio = api.portfolio.requests()
    positions = portfolio.positions
    portfolio.pop("positions")
    pp.pprint(dict(portfolio))

    print(utils.printable_banner('"Position" Endpoint (Summed positions)'))
    df = positions.to_pandas()
    df["total"] = df.apply(lambda x: Decimal(x["quantity"]) * x["offer.amount"], axis=1)
    assets = df["total"].sum()
    print(f"Total assets of portfolio (no currency convert, careful): {assets}")

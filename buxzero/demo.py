from config import load_config as load, load_token_opts

from _user import UserAPI

import utils

from pprint import PrettyPrinter

if __name__ == "__main__":

    pp = PrettyPrinter(indent=2)

    utils.read_environment_file()

    c = load(load_token_opts)

    api = UserAPI(config=c)

    #me = api.me.requests()
    #pd = api.personal_data.requests()
    portfolio = api.portfolio.requests()

    positions = portfolio.positions

    print([p.investment_amount for p in positions])
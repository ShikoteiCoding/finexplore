from argparse import ArgumentParser

import bux

from ._command import Command, register


@register
class Portfolio(Command):
    name = "portfolio"

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        parser.add_argument("--config", required=False)

    def run(self) -> int:
        if self.args.config:
            self.load_config_env(file_path=str(self.args.config))
        else:
            self.load_config_env()
        api = bux.UserAPI(config=self.config)
        portfolio = api.portfolio.requests()
        print(portfolio)
        return 0

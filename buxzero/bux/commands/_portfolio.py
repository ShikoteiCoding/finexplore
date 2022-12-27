from argparse import ArgumentParser

import bux
import json

from ._command import Command, register


@register
class Portfolio(Command):
    name = "portfolio"

    @staticmethod
    def init_parser(parser: ArgumentParser) -> None:
        parser.add_argument("-c", "--config", required=False)
        parser.add_argument(
            "-o",
            "--output",
            required=False,
            default="console",
            choices=["json", "console"],
        )

    def run(self) -> int:
        if self.args.config:
            self.load_config_env(file_path=str(self.args.config))
        else:
            self.load_config_env()

        api = bux.UserAPI(config=self.config)
        portfolio = api.portfolio.requests()

        if self.args.output == "json":
            print(json.dumps(dict(portfolio)))
        elif self.args.output == "console":
            print(portfolio)

        return 0

from config import load_config as load, load_token_opts

from _user import UserAPI

import utils


if __name__ == "__main__":

    utils.read_environment_file()

    c = load(load_token_opts)

    user = UserAPI(config=c)

    print(user.me().requests())

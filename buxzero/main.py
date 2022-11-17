from config import load_config as load, load_token_opts

from _user import UserAPI

from utils import get_or_create_token


if __name__ == "__main__":

    get_or_create_token()

    c = load(load_token_opts)

    user = UserAPI(config=c)

    print(user.me().requests())

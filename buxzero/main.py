from config import Config

from _user import UserAPI
from utils import get_token

if __name__ == "__main__":

    c = Config()

    token = get_token()
    user = UserAPI(token=token)

    print(user.me().requests())

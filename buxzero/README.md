# BuxZero API

BuxZero is a digital / neo broker. It is still not providing an open source API. Let's build mine.

## Credits

An API is already existing: https://github.com/orsinium-labs/bux
This sub-project is heavily inspired from the above open-sourced project. (Learning purposes).

## Build

It is best to encapsulate in a virtual environment. See the documentation for virtualenv: https://virtualenv.pypa.io/en/latest/
```shell
virtualenv venv
source venv/bin/activate
```

Install the dependencies
```shell
pip3 install -r requirements.txt
```

## Run

### Get Token

If you don't have a token yet:
```shell
python3 -m bux get-token
```

### Use Token
Once your token retrieved. Store it as an environment variable BUX_TOKEN in a file.
Default file location is :
```shell
$HOME/.bux-token.env
```

### Demo
In order to successfully run the demo, please make sure to have a token.env file in your root folder with your bux token stored inside.
```shell
python3 demo.py
```

## Test
```shell
pytest tests/test_config.py
pytest tests/test_user.py
```
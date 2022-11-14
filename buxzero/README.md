# BuxZero API

BuxZero is a digital / neo broker. It is still not providing an open source API. Let's build mine.

## Credits

An API is already installing from PyPi here: https://github.com/orsinium-labs/bux
My work will be inspired as the code structure is pretty beautiful and I will learn a lot from reproducing.
However I am not needing all their components for now so I will get straight to the point.

## Build

It is best to encapsulate a dedicated virtual environment. See the documentation for virtualenv: https://virtualenv.pypa.io/en/latest/
```shell
virtualenv venv
source venv/bin/activate
```

Install the dependencies
```shell
pip3 install -r requirements.txt
```

## Run

```shell
python3 main.py
```

## Test
```shell
python3 test.py
```
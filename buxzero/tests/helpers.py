import bux
from datetime import datetime
from jsonpath_ng import jsonpath, parse
from decimal import Decimal
from typing import Any
from bux.responses import Price

import pandas as pd


def format_prices_dicts(obj: dict) -> dict:
    """
    Transform dict with currency, decimals and amount keys to Price objects for comparison.
    """

    def format(item: Any) -> Any:
        for k, v in item.copy().items():
            if isinstance(v, dict):
                if v.get("currency") and v.get("decimals") and v.get("amount"):
                    item.pop(k)
                    item[k] = Price(v)
                else:
                    format(v)
        return item

    return format(obj)


def trim_root_keys(obj: dict, keys: set[str]):
    """
    Remove keys if they are in the root container.
    """
    output = obj.copy()
    for key in keys:
        output.pop(key)
    return output


def flatten_dict(obj: dict, sep: str = ".") -> dict:
    """
    Flat dictionnary nested keys.
    """
    output = {}

    def flatten(item: dict | list | Any, name: str = ""):
        if type(item) is dict:
            for a in item:
                flatten(item[a], name + a + sep)
        elif type(item) is list:
            i = 0
            for a in item:
                flatten(a, name + str(i) + sep)
                i += 1
        else:
            output[name[:-1]] = item

    flatten(obj)
    return output


def assert_fields_exist(response: bux.Response, fields: set[str] = set()):
    """
    Assert json paths exist in object.
    """
    uncalled = []
    for field in fields:
        json_path = parse(field)
        value = json_path.find(response)
        if not value:
            uncalled.append(field)
    assert not uncalled, "Missing fields: " + " ".join(uncalled)


def assert_fields_have_getters(
    response: bux.Response, exclude: set[str] = set(), pop: set[str] = set()
):
    """
    Assert all response fields have getters to access.
    """

    # Call each declared properties
    dict_methods = dir(dict)
    values = []
    for prop in dir(type(response)):
        if prop in dict_methods:
            continue
        if prop.startswith("_"):
            continue
        value = getattr(response, prop)
        if not value:
            continue
        values.append(value)

    # Remove root keys
    response_dict = trim_root_keys(dict(response), pop)

    # Compare response (key, values) to called properties values
    uncalled = []
    price_formatted = format_prices_dicts(response_dict)
    flat_formatted = flatten_dict(price_formatted)
    for key, value in flat_formatted.items():
        if key in exclude:
            continue
        if value not in values:
            uncalled.append(key)

    assert not uncalled, "Missing fields: " + " ".join(uncalled)

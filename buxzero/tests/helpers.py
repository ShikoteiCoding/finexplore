import bux
from datetime import datetime
from jsonpath_ng import jsonpath, parse
from decimal import Decimal
from typing import Any

import pandas as pd


def flatten_dict(obj: dict) -> dict:
    output = {}

    def flatten(item: dict | list | Any, name: str = ""):
        if type(item) is dict:
            for a in item:
                flatten(item[a], name + a + ".")
        elif type(item) is list:
            i = 0
            for a in item:
                flatten(a, name + str(i) + ".")
                i += 1
        else:
            output[name[:-1]] = item

    flatten(obj)
    return output


def assert_fields_exist(response: bux.Response, fields: set[str] = set()):
    """Assert json paths exist in object."""
    uncalled = []
    for field in fields:
        json_path = parse(field)
        value = json_path.find(response)
        if not value:
            uncalled.append(field)
    assert not uncalled, "Missing fields: " + " ".join(uncalled)


def assert_fields_have_getters(response: bux.Response, exclude: set[str] = set()):
    """Assert all response fields have getters to access."""

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

    # Compare response actual values to called properties values
    uncalled = []
    actual_values = []
    for key, value in flatten_dict(dict(response)).items():
        if key in exclude:
            continue
        actual_values.append(value)
        if value not in values:
            uncalled.append(key)

    # Check called property values not excluded are same as property values
    unfound = set(sorted(values)) - set(sorted(actual_values))

    # Check for nested fields
    assert not uncalled, "Missing fields: " + " ".join(uncalled)
    assert not unfound, "Property values not found: " + " ".join(unfound)

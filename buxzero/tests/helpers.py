import bux
from datetime import datetime

from decimal import Decimal

##############################
###### TODO: Should be able to check for nested fields and nest values nativelue. Use jsonpath-ng ?
##############################


def assert_fields_have_getters(response: bux.Response, exclude=(), unwrap=()):
    """ Assert all response fields have getters to access. """

    # Call each declared properties
    dict_methods = dir(dict)
    values = []
    for prop in dir(type(response)):
        if prop in dict_methods:
            continue
        if prop.startswith("_"):
            continue
        values.append(getattr(response, prop))

    # Compare actual values to called properties
    uncalled = []
    for key, value in response.items():
        if key in exclude:
            continue
        if key in unwrap:
            continue
        if value not in values:
            uncalled.append(key)

    # Check for nested fields
    for subkey in unwrap:
        for key, value in response[subkey].items():
            if key in exclude:
                continue
            if key in unwrap:
                continue
            if value not in values:
                uncalled.append(key)

    assert not uncalled, "Missing fields: " + ' '.join(uncalled)
import bux
from datetime import datetime

from decimal import Decimal

def check_has_properties(response: bux.Response, methods: list[str]):
    obj_attrs = dir(response)

    # Check methods exist
    for method in methods:
        assert method in obj_attrs
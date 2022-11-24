import sys
sys.path.append("..")
import bux

def check_properties(response: bux.Response, methods: list[str]):
    obj_attrs = dir(response)
    print(obj_attrs)
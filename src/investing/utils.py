import json
import pprint

def load_json(path: str) -> dict:
    with open(path) as f:
        content = json.load(f)
    return content
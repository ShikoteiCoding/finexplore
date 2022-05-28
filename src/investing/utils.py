import json
import pprint

def load_json(path: str, **kwargs) -> dict:
    with open(path, **kwargs) as f:
        content = json.load(f)
    return content
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

import os

@dataclass
class Config:
    
    db_username:str = field(default="")
    db_password:str = field(default="")
    db_name:str = field(default="")
    db_host:str = field(default="")
    db_port:str = field(default="")
    polygon_access_key:str = field(default="")

def load_config(*opts:Callable) -> Config:
    c = Config()

    for opt in opts:
        opt(c)

    return c

def load_db_opts(config: Config) -> None:
    config.db_username = os.getenv("POSTGRES_USERNAME", "")
    config.db_password = os.getenv("POSTGRES_PASSWORD", "")
    config.db_name = os.getenv("POSTGRES_DB_NAME", "")
    config.db_host = os.getenv("POSTGRES_DB_HOST", "")
    config.db_port = os.getenv("POSTGRES_DB_PORT", "")

def load_polygon_opts(config: Config) -> None:
    config.polygon_access_key = os.getenv("POLYGON_ACCESS_KEY", "")
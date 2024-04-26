import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    user: str
    password: str
    address: str
    name: str


@dataclass
class Config:
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes", "y")


def load_config(path: str):
    config_ = configparser.ConfigParser()
    config_.read(path)

    return Config(
        db=DbConfig(**config_["db"]),
    )


config = load_config("config.ini")

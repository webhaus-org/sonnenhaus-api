import dacite
import dataclasses
import yaml


@dataclasses.dataclass
class Db:
    db_url: str


@dataclasses.dataclass
class Github:
    webhook_secret: str


@dataclasses.dataclass
class Server:
    service_name: str


@dataclasses.dataclass
class Config:
    db: Db
    github: Github
    server: Server


def make_config_obj(cfg_file: str):
    if not cfg_file:
        raise Exception("Mssing configuration file")

    with open(cfg_file, "r") as f:
        return dacite.from_dict(data_class=Config, data=yaml.safe_load(f))

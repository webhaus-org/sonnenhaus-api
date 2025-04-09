import dacite
import dataclasses
import yaml


@dataclasses.dataclass
class Db:
    db_url: str


@dataclasses.dataclass
class Config:
    db: Db


def make_config_obj(cfg_file: str):
    if not cfg_file:
        raise Exception("Mssing configuration file")

    with open(cfg_file, "r") as f:
        return dacite.from_dict(data_class=Config, data=yaml.safe_load(f))

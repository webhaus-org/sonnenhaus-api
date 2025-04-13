import dacite
import dataclasses
import yaml


@dataclasses.dataclass
class Db:
    db_url: str


@dataclasses.dataclass
class AuthenticationService:
    authentication_provider: str
    path_to_authentication_provider_config: str


@dataclasses.dataclass
class Server:
    authentication_service: AuthenticationService


@dataclasses.dataclass
class MeasurementValidation:
    path_to_public_key: str


@dataclasses.dataclass
class Measurement:
    validation: MeasurementValidation


@dataclasses.dataclass
class Config:
    db: Db
    server: Server
    measurement: Measurement


def make_config_obj(cfg_file: str):
    if not cfg_file:
        raise Exception("Mssing configuration file")

    with open(cfg_file, "r") as f:
        return dacite.from_dict(data_class=Config, data=yaml.safe_load(f))

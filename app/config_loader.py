import yaml
from pydantic import BaseModel


class BaseConfig(BaseModel):
    DB_DATABASE: str
    DB_LOGIN: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    SERVER_HOST: str
    SERVER_PORT: int
    APP_KEY: str


def load_conf():
    with open("config.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return BaseConfig.parse_obj(data)
        except yaml.YAMLError as exp:
            raise Exception("could not load config file")


config = load_conf()

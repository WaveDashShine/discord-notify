import os
from dotenv import load_dotenv
import yaml
from enum import StrEnum
from dataclasses import dataclass


# environment variables
load_dotenv()
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID"))


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class SiteKeys(StrEnum):
    ASURA = "asura"
    FLAME = "flame"


class SiteDataKeys(StrEnum):
    URL = "url"
    TITLE_LIST = "manhwa"


@dataclass
class SiteData:
    def __init__(self, yaml_data: dict):
        self.url: str = yaml_data.get(SiteDataKeys.URL)
        self.titles: list = yaml_data.get(SiteDataKeys.TITLE_LIST)
        self.validate_data()

    def validate_data(self):
        if not self.url:
            raise RuntimeError(f"Missing URL to manhwa website in yaml data")


class ManhwaConfig:
    def __init__(self, yaml_data: dict):
        self.data: dict = yaml_data
        self.asura: SiteData = SiteData(yaml_data=yaml_data.get(SiteKeys.ASURA))
        self.flame: SiteData = SiteData(yaml_data=yaml_data.get(SiteKeys.FLAME))


def load_yaml():
    file_path: str = os.path.join(ROOT_PATH, "manhwa_config.yaml")
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)  # Use safe_load to prevent arbitrary code execution
    return ManhwaConfig(yaml_data=data)


MANHWA_CONFIG: ManhwaConfig = load_yaml()

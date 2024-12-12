import os
import csv
import json
import httpx
import logging

from enum import StrEnum
from base64 import b64encode
from datetime import datetime
from dotenv import load_dotenv
from dataclasses import asdict
from sys import version as SYS_VERSION
from logging.handlers import TimedRotatingFileHandler

timestamp = datetime.now().strftime("%Y-%m-%d")

LOG_DIR = os.path.join("../", "Logs")
LOG_FILE = os.path.join(LOG_DIR, f"sniffgalon_{timestamp}.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

__logger = logging.getLogger("sniffgalon")
__logger.setLevel(logging.DEBUG)
log_format = logging.Formatter("[%(asctime)s]:[%(levelname)s:%(name)s]: %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.DEBUG)

__logger.addHandler(console_handler)  # adds console handler to our logger

file_handler = TimedRotatingFileHandler(
    filename=LOG_FILE, encoding="utf-8", when="midnight", backupCount=30
)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.DEBUG)

__logger.addHandler(file_handler)  # adds filehandler to our logger

__logger.info(f"Using Python version {SYS_VERSION}")

load_dotenv()

API_URL = "https://us.api.blizzard.com/data/wow"
API_TOKEN_URL = "https://us.battle.net/oauth/token"

# grabs your blizzard API ID and secret from the .env file (placed in the base directory, above Sniffer/)
# if you don't wanna mess with a .env file, just set them here
CLIENT_ID = os.getenv("BLIZZARD_API_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLIZZARD_API_CLIENT_SECRET")

LOCALE = "en_US"
REGION = "us"
USER_AGENT = "AlgalonGhost"


class BattleNetNamespace(StrEnum):
    STATIC = "static-us"
    DYNAMIC = "dynamic-us"
    PROFILE = "profile-us"

    STATIC_ERA = "static-classic1x-us"
    DYNAMIC_ERA = "dynamic-classic1x-us"
    PROFILE_ERA = "profile-classic1x-us"

    STATIC_LK = "static-classic-us"
    DYNAMIC_LK = "dynamic-classic-us"
    PROFILE_LK = "profile-classic-us"


def get_access_token() -> str:
    body = {"grant_type": "client_credentials"}
    headers = {
        "Authorization": f"Basic {b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')}",
        "User-Agent": USER_AGENT,
    }

    with httpx.Client(http2=True) as client:
        try:
            response = client.post(API_TOKEN_URL, headers=headers, data=body)
        except Exception:
            __logger.error("Encountered an error during authentication", exc_info=True)
            return

        if response.status_code == 200:
            return response.json()["access_token"]


def get_headers(access_token, namespace: BattleNetNamespace) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Battlenet-Namespace": namespace,
        "locale": LOCALE,
        "region": REGION,
        "User-Agent": USER_AGENT,
    }

    return headers


def process_file_path_and_make_dirs(file_path: str) -> str:
    file_path = file_path.replace("\\", "/").replace(" ", "")
    folder_path = os.path.split(file_path)[0]
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return file_path


def dump_csv(file_path: str, data: dict) -> None:
    file_path = process_file_path_and_make_dirs(file_path)

    with open(file_path, "w", newline="") as file:
        csv_writer = csv.writer(file)
        header = data[0].keys()
        csv_writer.writerow(header)

        for category in data:
            csv_writer.writerow(category.values())

    __logger.info(f"CSV data dumped to {file_path}")


def dump_json(file_path: str, json_data: dict) -> None:
    file_path = process_file_path_and_make_dirs(file_path)

    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)
        __logger.info(f"JSON data dumped to {file_path}")


def compress_generic_dict(data: list) -> list[dict[str, str]]:
    new_data = []
    for dataset in data:
        new_dataset = {
            "id": dataset["id"],
            "name": dataset["name"][LOCALE],
            "href": dataset["key"]["href"],
        }
        new_data.append(new_dataset)

    return new_data


class BaseDumper:
    name: str
    path: str  # the "area" part of the URL that'll be used for requests
    dump_path: str
    logger: logging.Logger
    client: httpx.Client
    dict_key: str
    dump_raw: bool
    dump_processed: bool
    override_index_endpoint: str | None = None
    override_key_name: str | None = None
    request_count: int = 0
    object_class: object | None = None

    @classmethod
    def new(
        cls,
        name: str,
        path: str,
        dump_raw: bool = False,
        dump_processed: bool = False,
        override_index_endpoint: str | None = None,
        override_key_name: str | None = None,
        object_class: object | None = None,
    ):
        dump_path = f"../Data/{timestamp}/{name}"
        logger = logging.getLogger(f"sniffgalon.{name.lower()}")

        access_token = get_access_token()

        client = httpx.Client(
            http2=True,
            headers=get_headers(access_token, BattleNetNamespace.STATIC),
        )

        dumper = cls()
        dumper.name = name
        dumper.path = path
        dumper.dump_path = dump_path
        dumper.logger = logger
        dumper.client = client

        dumper.override_key_name = override_key_name
        dumper.dict_key = dumper.override_key_name or dumper.name.lower()

        dumper.dump_raw = dump_raw
        dumper.dump_processed = dump_processed
        dumper.override_index_endpoint = override_index_endpoint

        if not dumper.object_class:
            dumper.object_class = object_class

        return dumper

    def fetch_index(
        self, override_dict_key: str | None = None
    ) -> list[dict[str, str]] | None:
        self.logger.info(f"Fetching {self.name} index...")

        if self.override_index_endpoint:
            url = f"{API_URL}{self.override_index_endpoint}"
        else:
            url = f"{API_URL}/{self.path}/index"

        response = self.client.get(url)

        if response.status_code != 200:
            self.logger.error(
                f"Error occurred fetching {self.name} index with code {response.status_code}"
            )
            return

        self.request_count += 1
        data = response.json()

        if self.dump_raw:
            file_name = f"{self.dump_path}/Raw/{self.name}_Index.json"
            dump_json(file_name, data)

        key = override_dict_key or self.dict_key
        processed = compress_generic_dict(data[key])

        if self.dump_processed:
            file_name = f"{self.dump_path}/Processed/{self.name}_Index.csv"
            dump_csv(file_name, processed)

        return processed

    def fetch_specific(self, id: int):
        if not self.object_class:
            self.logger.error(f"No object_class set for {self.name} dumper.")
            return

        self.logger.info(f"Fetching {self.name} with ID {id}...")

        url = f"{API_URL}/{self.path}/{id}"
        response = self.client.get(url)

        if response.status_code != 200:
            self.logger.error(
                f"Failed to fetch {self.name} ID {id} with code {response.status_code}"
            )
            return

        self.request_count += 1
        data = response.json()

        if self.dump_raw:
            file_name = f"{self.dump_path}/Specific/{self.name}_{id}.json"
            dump_json(file_name, data)

        return self.object_class.from_json(data)

    def fetch_many(self, ids: list[int]):
        all_results = [self.fetch_specific(id=id) for id in ids]
        return all_results

    def fetch_all(self):
        return self.fetch_index()

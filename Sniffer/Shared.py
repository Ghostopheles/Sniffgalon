import os
import csv
import json
import httpx
import logging

from datetime import datetime
from sys import version as SYS_VERSION
from dotenv import load_dotenv
from enum import StrEnum
from base64 import b64encode
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

API_URL = "https://us.api.blizzard.com"
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


def get_access_token() -> str:
    body = {"grant_type": "client_credentials"}
    headers = {
        "Authorization": f"Basic {b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')}",
        "User-Agent": USER_AGENT,
    }

    with httpx.Client(http2=True) as client:
        try:
            response = client.post(API_TOKEN_URL, headers=headers, data=body)
        except Exception as exc:
            __logger.error("Encountered an error during authentication")
            __logger.error(exc)
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
    def __init__(self, name: str):
        self.dump_path = f"../Data/{timestamp}/{name}"
        self.logger = logging.getLogger(f"sniffgalon.{name.lower()}")

        access_token = get_access_token()

        self.client = httpx.Client(
            http2=True,
            headers=get_headers(access_token, BattleNetNamespace.STATIC),
        )

        self.request_count = 0

#!/usr/bin/env python3

from curses.ascii import HT
import os
from datetime import datetime
import logging
import time
import requests
from requests.auth import HTTPBasicAuth
from prometheus_client import start_http_server, Gauge


class Tailscale:
    def __init__(self, tailnet: str, api_key: str):
        self.tailnet = tailnet
        self.api_key = api_key
        self.gauge_total_devices = Gauge(
            name="tailscale_total_devices", documentation="Total devices"
        )

    def devices(self):
        req = requests.get(
            headers={
                "Content-type": "application/json",
            },
            url=f"https://api.tailscale.com/api/v2/tailnet/{self.tailnet}/devices",
            auth=HTTPBasicAuth(self.api_key, None),
            timeout=10,
        )
        if not req.ok:
            raise RuntimeError(f"req not ok {req.status_code}: {req.text}")

        req_json = req.json()
        if not req_json:
            raise RuntimeError("no json")

        devices = req_json.get("devices")
        if not devices:
            raise RuntimeError("no devices")

        self.gauge_total_devices.set(len(devices))

        return req_json


def env_value(name, default=None):
    """
    Given the name of an env var key, returns the value inside the name with the
    _FILE suffix (if it exists), otherwise returns the value of the named env
    key.  If the key does not exists, returns the default value.

    If the referenced file does not exist, will throws a FileNotFoundError.
    """
    envfile_key = f"{name}_FILE"
    if envfile_key in os.environ:
        with open(os.environ[envfile_key], "r") as envfile:
            # read will return the string followed by a newline, which we don't
            # want so we split and take the first line without the \n
            return envfile.read().splitlines()[0]
    else:
        return os.getenv(name, default)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    EXPORTER_PORT = int(env_value("EXPORTER_PORT", "8000"))
    POLLING_INTERVAL = int(env_value("POLLING_INTERVAL", "60"))

    tailscale = Tailscale(
        tailnet=env_value("TAILSCALE_TAILNET"),
        api_key=env_value("TAILSCALE_API_KEY"),
    )

    start_http_server(port=EXPORTER_PORT, addr="0.0.0.0")
    while True:
        json = tailscale.devices()
        logging.info("%s:%s", datetime.now(), json)
        time.sleep(POLLING_INTERVAL)

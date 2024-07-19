#! /usr/bin/env python3

import docker
import requests

from utils import get_node, Status
from tx import update_status


def listen():
    client = docker.client.from_env()
    for event in client.events(decode=True):
        if "status" in event and event["status"] == "die":
            cwd = event["Actor"]["Attributes"]["com.docker.compose.project.working_dir"]
            requests.post("http://localhost:8000/stop", params={"node_id": get_node(cwd)})
            update_status(node_id=int(get_node(cwd)), status=Status.ERROR.value)


if __name__ == "__main__":
    listen()

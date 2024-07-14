from enum import Enum


class Status(Enum):
    QUEUED = 0
    RUNNING = 1
    STOPPING = 2
    DOWN = 3
    ERROR = 4


def get_path(node_id: str) -> str:
    return f"./node-{node_id}/"


def get_node(path: str) -> str:
    return path.split("-")[-1]

"""
not a library for gas, this stands for Get And Store
"""

import json
import io


def get(fn: str) -> io.TextIOWrapper:
    with open(fn) as file:
        return json.load(file)


def store(fn: str, things: dict):
    with open(fn, "w") as file:
        json.dump(things, file)
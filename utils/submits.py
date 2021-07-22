from typing import Any
from submits import submits, approved_submits


class Queue:
    def __init__(self):
        self.__items: list[dict[str, Any]] = {}

    @property
    def items(self):
        return self.__items

    @items.getter
    def items(self):
        return sorted(self.__items, key=lambda item: item["timestamp"])

    def init(self):
        self.__items = [{"id": i.id, "timestamp": i.date} for i in submits]

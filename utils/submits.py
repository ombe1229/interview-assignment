from typing import Any, Optional
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

    def init(self) -> None:
        self.__items = [{"id": i.id, "timestamp": i.date} for i in submits]

    def find_by_id(self, id: int) -> dict[str, Any]:
        return list(filter(lambda item: item["id"] == id, self.__items))[0]

    def perform(self, bot: dict[str, Any], approve: Optional[bool] = None) -> None:
        self.__items.remove(bot)
        item = list(filter(lambda item: item.id == bot["id"], submits))[0]
        submits.remove(item)
        if approve:
            approved_submits.append(item)
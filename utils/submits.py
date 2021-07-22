from typing import Any, NoReturn
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

    def init(self) -> NoReturn:
        self.__items = [{"id": i.id, "timestamp": i.date} for i in submits]

    def find_by_id(self, id: int) -> dict[str, Any]:
        return list(filter(lambda item: item["id"] == id, self.__items))[0]

    def approve(self, bot: dict[str, Any]) -> NoReturn:
        self.__items.remove(bot)
        for i in submits:
            if i.id == bot["id"]:
                submits.remove(i)
                approved_submits.append(i)
                break

    def deny(self, bot: dict[str, Any]) -> NoReturn:
        self.__items.remove(bot)
        for i in submits:
            if i.id == bot["id"]:
                submits.remove(i)
                break

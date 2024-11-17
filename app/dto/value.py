from typing import List


class ValueDto:
    def __init__(self, title: str, name: str, values: List[int]):
        self.title = title
        self.name = name
        self.values = values

    def __str__(self):
        return f"{self.title}: {self.name}"
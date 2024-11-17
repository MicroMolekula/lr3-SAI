from typing import List

from app.dto.value import ValueDto


class CoefDto:
    def __init__(self, title: str, name: str, coefs: List[float]):
        self.title = title
        self.name = name
        self.coefs = coefs

    def __str__(self):
        return f"title: {self.title}, name: {self.name}, coefs: {self.coefs}"

    def text(self, value: ValueDto) -> str:
        return f"{value.name} - {self.name}\n\t{self.title} = {' + '.join([f"{value.values[i]}/{self.coefs[i]}" for i in range(len(self.coefs))])}"
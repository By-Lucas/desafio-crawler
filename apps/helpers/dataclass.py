from dataclasses import dataclass


@dataclass
class Quote:
    text:str
    author: str
    birth_date: str
    birth_place: str
    description: str
    tags: list

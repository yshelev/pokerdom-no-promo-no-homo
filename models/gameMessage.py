from dataclasses import dataclass

@dataclass
class GameMessage:
    data: list[int]
    action: str
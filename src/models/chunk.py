from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    embedding: list[float]
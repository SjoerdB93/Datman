from dataclasses import dataclass, field

@dataclass
class dataset:
    x_data: list[float] = None
    y_data: list[float] = None

    def __init__(self):
        pass
from dataclasses import dataclass, field

@dataclass
class Data:
    xdata: list[float] = field(default_factory=list)
    ydata: list[float] = field(default_factory=list)
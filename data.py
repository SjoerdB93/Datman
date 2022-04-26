from dataclasses import dataclass, field

@dataclass
class Data:
    filename: str = ""
    xdata: list[float] = field(default_factory=list)
    ydata: list[float] = field(default_factory=list)
    xdata_selected: list[float] = field(default_factory=list)
    ydata_selected: list[float] = field(default_factory=list)

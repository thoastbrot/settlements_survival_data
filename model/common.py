# -*- coding: utf-8 -*-
from dataclasses import dataclass

from dataclasses_json import dataclass_json


class LocalizedString(str):
    ...


# TODO: is assigned as list, but can't be declared as such...
class SingleValues:
    ...


@dataclass_json
@dataclass
class Range:
    Lower: int
    Upper: int

    def avg(self) -> float:
        avg = (self.Upper + self.Lower)/2
        return round(avg) if round(avg) == avg else avg

    def __str__(self):
        if self.Lower == self.Upper:
            return str(self.Lower)
        else:
            return f"{self.Lower}-{self.Upper}"

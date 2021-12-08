# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

from model.common import SingleValues, LocalizedString


class Type(SingleValues):
    values: int


@dataclass_json
@dataclass
class ItemType:
    ID: int
    Name: LocalizedString
    LittleIcon: str
    DefaultUpper: int
    WarnNum: int
    FirstType: int
    TypeList: Type


@dataclass_json
@dataclass
class Item:
    ID: int
    Icon: str
    Name: LocalizedString
    Des: LocalizedString
    Limit: int
    Worth: int
    Weight: int
    OrderWorth: int
    Height: float
    Priority: LocalizedString
    IsBan: bool
    OutputBuilding: List[int]
    ToUnlockTech: int
    # ItemsAttributes: Attributes List of Int1, Int2, Int3... useless?
    # TypeList for classification into FoodLow/FoodMiddle/...

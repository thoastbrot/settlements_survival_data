# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

from model.common import LocalizedString, Range


@dataclass_json
@dataclass
class TemperatureRange:
    Lower: int
    Upper: int

    def __str__(self):
        if self.Lower == self.Upper:
            return f"{self.Lower} °F"
        else:
            return f"{self.Lower}-{self.Upper} °F"


@dataclass_json
@dataclass
class FinishRes:
    ID: int
    NumRange: Optional[Range]
    UnEducatedNumRange: Optional[Range]
    RandomRange: int
    UnlockTech: int
    Rate: int


@dataclass_json
@dataclass
class LifeCircle:
    MinSize: float
    MaxSize: float
    Grow: int
    DeadRange: Optional[Range]


@dataclass_json
@dataclass
class ResourceAttributes:
    ID: int
    Name: LocalizedString
    canOverlay: bool
    LifeCircle: Optional[LifeCircle]
    FinishResList: List[FinishRes]
    # commented out in the XML
    # NatureDeadResList: List[NatureDeadRes]
    EntityType: int
    ActionType: int
    # Probability of Successful Acquisition (%)
    CreateRate: int
    DependMature: bool
    FruitAction: int
    # See IDs in the citizenaction
    FruitID: int
    RipeDays: int
    NumRange: Optional[Range]
    # Temperature Range for Fruit Output (F)
    FruitGrowTmc: Optional[TemperatureRange]
    # Temperature Range for Survival (F)
    DeadTmc: Optional[TemperatureRange]
    # Temperature Range for Growth (F)
    GrowTmc: Optional[TemperatureRange]

    @property
    def EntityTypeName(self) -> str:
        return {
            1: "tree",
            2: "stone",
            3: "iron",
            4: "plant",
            5: "herb",
            6: "build",
            7: "road",
            8: "boat",
            9: "animal",
            10: "tomb",
            11: "wildAnim",
            12: "fruitTree",
            13: "crop",
        }.get(self.EntityType, f"unknown: {self.EntityType}")


@dataclass_json
@dataclass
class Seed:
    ID: int
    Name: LocalizedString
    Des: LocalizedString
    Icon: str
    OutputPath: LocalizedString
    ResID: int
    IsStartRandom: bool
    BuildingFuncType: int
    Offset: float
    Worth: int
    SellValue: int


@dataclass_json
@dataclass
class Produce:
    ID: int
    NumRange: Optional[Range]


@dataclass_json
@dataclass
class Animal:
    ID: int
    Name: LocalizedString
    Des: LocalizedString
    Icon: str
    OutputPath: LocalizedString
    ResID: int
    ProduceList: List[Produce]
    # WorkRequired not understood yet
    StartAnimalNum: Optional[Range]
    AnimalBornAgeRange: Optional[Range]
    NeedFodder: int
    FodderAddAge: int
    Worth: int
    SellVaue: Optional[Range]

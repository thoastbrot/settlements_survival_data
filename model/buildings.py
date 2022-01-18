# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

from model.common import LocalizedString, Range, SingleValues


@dataclass_json
@dataclass
class ConsumMaterials:
    ID: int
    Num: int


@dataclass_json
@dataclass
class Goods:
    ID: int
    UnEducated: int
    Educated: int


@dataclass_json
@dataclass
class ConsumeAddAbility:
    ID: int
    Lable: LocalizedString
    ConsumMaterialsList: List[ConsumMaterials]
    ProduceType: List[Goods]
    SeedId: int
    UnlockTech: int
    WorkRequired: int


@dataclass_json
@dataclass
class ItemWithAmount:
    ID: int
    Num: int


@dataclass_json
@dataclass
class AllConsumRes(ItemWithAmount):
    ...


@dataclass_json
@dataclass
class MeshConsumeRes(ItemWithAmount):
    ...


@dataclass_json
@dataclass
class ResStorageNum:
    ID: int
    Rate: float


@dataclass_json
@dataclass
class WorkerRange(Range):
    ...


@dataclass_json
@dataclass
class BuildingDimension:
    x: int
    z: int


@dataclass_json
@dataclass
class MinSize(BuildingDimension):
    ...


@dataclass_json
@dataclass
class MaxSize(BuildingDimension):
    ...


@dataclass_json
@dataclass
class DragSize:
    MinSize: Optional[MinSize]
    MaxSize: Optional[MaxSize]


@dataclass_json
@dataclass
class FixedSize:
    Condition: str
    Attach: str

    # TODO... how to make things work
    @property
    def size(self):
        rows = self.Condition.strip().split()
        return [len(rows), len(rows[0].split(","))]


class TypeStorage(SingleValues):
    values: int


class Upgrade(SingleValues):
    values: int


class CanKeepAnimal(SingleValues):
    values: int


@dataclass_json
@dataclass
class Building:
    ID: int
    Icon: str
    ContentDes: LocalizedString
    RemouldSlot: int
    ViewType: int
    FuncType: int
    Name: LocalizedString
    Des: LocalizedString
    Order: int
    # Items for building
    MeshConsumeResList: List[MeshConsumeRes]
    AllConsumResList: List[AllConsumRes]
    ConsumeAddAbilityList: List[ConsumeAddAbility]
    # WorkRequired: Tuple[int, int, int]  # TODO update data then
    #  Single grid requires work character coefficient
    MeshNeedWorker: float
    StorageLimit: int
    # items for repairing
    FixStaff: Optional[ItemWithAmount]
    # the ratio of item types to attempt to store in the buildings
    ResStorageNumList: List[ResStorageNum]
    WorkerRange: Optional[WorkerRange]
    # FixedSize grid contains ground type to build on:
    # 1 is plain ground,
    # 4 is water,
    # 7 is water or plain ground,
    # 5 is mountain,
    # 6 is mountain or plain ground.
    FixedSize: Optional[FixedSize]
    DragSize: Optional[DragSize]
    UpgradeList: Upgrade
    TypeStorageList: TypeStorage
    CanKeepAnimalList: CanKeepAnimal

    # Feature Type Enumeration from the xml docs
    @property
    def FuncTypeName(self):
        return {
            0: "Undefined",
            1: "Residence",
            2: "Warehouse",
            3: "Production",
            4: "Processing",
            5: "Range Collection Type",
            6: "Farmland",
            7: "Orchard",
            8: "Pasture",
            9: "Potion house",
            11: "School",
            12: "Hospital",
            13: "Church",
            14: "Cemetery",
            15: "Hunting house",
            16: "Market",
            17: "Forest hut",
            18: "City hall",
            19: "Trade station",
            20: "Science and technology laboratory",
            22: "Recycling shop",
            23: "Bonfire",
            24: "Honey house",
            25: "Study house",
            26: "Transit station",
            27: "Packaging plant",
            28: "Goods transit station Supplying building",
            29: "Science and technology laboratory Research institute",
            30: "Bathhouse",
            31: "Land trade station",
            32: "Magicbox",
            33: "event  Random event",
            34: "Repair shop",
            35: "Boiler room",
            36: "Police station",
            37: "Shelter",
            40: "Restaurant",
            41: "Type of standing work",
            50: "Road",
            100: "Decorative buildings",
        }.get(self.FuncType)


@dataclass_json
@dataclass
class TonwBuilding:
    Name: LocalizedString
    BuildingID: List[int]


@dataclass_json
@dataclass
class LogBuilding:
    Name: LocalizedString
    BuildingID: List[int]


@dataclass_json
@dataclass
class CommonSet:
    TonwBuildingList: List[TonwBuilding]
    LogBuildingList: List[LogBuilding]

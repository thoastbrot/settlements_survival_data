# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

# PEP8 properties should be lowercase: ignore

# TODO: integrate findings from https://stackoverflow.com/questions/51079503/dataclasses-and-property-decorator
# TODO: fix RuntimeWarning from dataclasses for non-optional values set to null
#  (wrapping with Optional will probably need changes to int/float/str types processing)


@dataclass_json
@dataclass
class Lang:
    LangType: str
    LangValue: str


@dataclass_json
@dataclass
class LangConfig:
    ID: str
    LangList: List[Lang]

    def get_by_language(self, language: str) -> List[Lang]:
        return [la for la in self.LangList if la.LangType == language]


class LocalizedString(str):
    ...


# TODO: is assigned as list, but can't be declared as such...
class SingleValues:
    ...


class TechId(SingleValues):
    values: int


@dataclass_json
@dataclass
class TechnologyModule:
    ID: int  # The technology module ID is unique and corresponds to the module ID in HardTechnology
    Name: LocalizedString  # The Name of the Technology Module
    IndustryType: int  # # The technology type in the corresponding enumeration
    Icon: str  # The File Name of Technology Module Icon
    Idx: int  # Consistent with IndustryType
    RowCount: int  # How many lines in total are there on this technology module page
    ClomnCount: int  # How many columns in total are there on this technology module page
    TechIdList: TechId  # IDs of all technology included in the module in no particular order
    ShowWin: bool  # Is the module displayed in the interface

    """
    Technology Type Enumeration
    IndustryType_Trade=  1;  // 贸易
    // Trade
    IndustryType_Education=  2;  // 教育
    // Education
    IndustryType_Mine=  3;  // 矿物
    // Minerals
    IndustryType_Build=  4;  // 建造
    // Construction
    IndustryType_Farming=  5;  // 农业
    // Agriculture
    IndustryType_Processing=  6;  // 加工业
    // Processing Industry
    IndustryType_Express=  7;  // 物流
    // Logistics
    IndustryType_Home=  8;  // 宜居
    // Good for living
    IndustryType_Moai=  9;  // 复活节岛专属
    // Exclusively for the Easter Island
    """


class PreTech(SingleValues):
    values: int


class UnlockBuffs(SingleValues):
    values: int


class HintTech(SingleValues):
    values: int


class UnlockBuildings(SingleValues):
    values: int


@dataclass_json
@dataclass
class Position:
    Int1: int
    Int2: int


@dataclass_json
@dataclass
class TechDescribe:
    Name: LocalizedString
    Content: LocalizedString


@dataclass_json
@dataclass
class Technology:
    ID: int
    Name: LocalizedString
    TechModule: int
    NeedPoint: int
    PreTechList: PreTech
    UnlockBuffsList: UnlockBuffs
    HintTechList: HintTech
    UnlockBuildingsList: UnlockBuildings
    Position: Optional[Position]
    TechDescribeList: List[TechDescribe]


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
class Range:
    Lower: int
    Upper: int

    def __str__(self):
        if self.Lower == self.Upper:
            return str(self.Lower)
        else:
            return f"{self.Lower}-{self.Upper}"


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
class DeadRange(Range):
    ...


@dataclass_json
@dataclass
class NumRange(Range):
    ...


@dataclass_json
@dataclass
class UnEducatedNumRange(Range):
    ...


@dataclass_json
@dataclass
class FruitGrowTmc(TemperatureRange):
    ...


@dataclass_json
@dataclass
class GrowTmc(TemperatureRange):
    ...


@dataclass_json
@dataclass
class DeadTmc(TemperatureRange):
    ...


@dataclass_json
@dataclass
class FinishRes:
    ID: int
    NumRange: Optional[NumRange]
    UnEducatedNumRange: Optional[UnEducatedNumRange]
    RandomRange: int
    UnlockTech: int
    Rate: int


@dataclass_json
@dataclass
class LifeCircle:
    MinSize: float
    MaxSize: float
    Grow: int
    DeadRange: Optional[DeadRange]


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
    NumRange: Optional[NumRange]
    # Temperature Range for Fruit Output (F)
    FruitGrowTmc: Optional[FruitGrowTmc]
    # Temperature Range for Survival (F)
    DeadTmc: Optional[DeadTmc]
    # Temperature Range for Growth (F)
    GrowTmc: Optional[GrowTmc]

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
class ConsumeAddAbility:
    ID: int
    Lable: LocalizedString
    ConsumMaterialsList: List[ConsumMaterials]
    ProduceType: List[Goods]
    SeedId: int
    UnlockTech: int


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
class WorkerRange:
    Lower: int
    Upper: int


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


@dataclass_json
@dataclass
class Upgrade(SingleValues):
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
    UpgradeList: List[Upgrade]

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
class CommonSet:
    TonwBuildingList: List[TonwBuilding]

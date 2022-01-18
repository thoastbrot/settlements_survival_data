# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Tuple, Optional, Union, Any

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

    @property
    def TypeNames(self) -> list[int]:
        mapping = {
            0: "Unknow",
            1: "Edible",  # 食物  Food
            2: "FoodLow",  # 低级  Low
            3: "FoodMiddle",  # 中级  Intermediate
            4: "FoodHigh",  # 高级  Advanced
            11: "Water",  # 水  Water
            21: "Health",  # 药品  Drugs
            22: "HealthCare",  # 保健品  Healthcare products
            23: "Treatment",  # 治疗药品  Therapeutic drugs
            31: "Wood",  # 木材（原料）  Lumber (raw material)
            32: "Log",  # 原木（木料）  Raw wood (wood material)
            33: "Timber",  # 木料（食品原料）  Wooden materials (food raw materials)
            34: "TextileMaterial",  # 纺织原料（纺织原料）  Textile raw materials (textile raw materials)
            35: "DrinkMaterial",  # 饮品原料（饮品原料）    Drinking ingredients (beverage raw materials)
            41: "Ragstone",  # 石材（建材）  Stone materials (construction materials)
            51: "Iron",  # 铁矿（矿物）  Ore (mineral)
            61: "Textile",  # 纺织品（服装）  Textiles (apparels)
            62: "Clothing",  # 衣物  Clothing
            63: "Fabric",  # 织物    Fabric
            64: "Backpack",  # 背包    Backpack
            65: "Shoes",  # 鞋子    Shoes
            71: "TreasuresMaterial",  # 珍品原料（贸易）  Precious ingredients (trade)
            301: "CoalFuel",  # 生活燃料（燃料）  Domestic fuel (fuel)
            311: "SmeltFuel",  # 工业燃料（燃料）  Industrial fuel (fuel)
            511: "Tool",  # 工具  Tools
            801: "Luxury",  # 奢侈品（饮品）  Luxury drinks (beverages)
            802: "Alcohol",  # 酒精（初级饮品）  Alcohol (primary drink)
            803: "HighEdible",  # 高级食物（中级饮品）  Advanced food (moderate drink)
            804: "HighColthing",  # 高级衣服（高级饮品）  Advanced Clothing (Advanced Drink)
            1001: "Seed",  # 种子  Seeds
            1002: "Livestock",  # 畜牧  Pasturage
            1101: "Coin",  # 金币  Gold Coin
            1102: "TechPoint",  # 科技  Technology
            1103: "BuildingDrawing",  # 工程图纸 蓝图  Engineering drawings and blueprint
        }
        return [mapping.get(i) for i in self.TypeList]


@dataclass_json
@dataclass
class Attributes:
    Int1: int
    Int2: int


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
    # TypeList for classification into FoodLow/FoodMiddle/... references ItemType(s)
    TypeList: Type
    # attributes with a value
    ItemsAttributes: List[Attributes]

    @property
    def ItemAttributesWithName(self) -> list[tuple[Optional[str], int]]:
        mapping = {
            1: "Eat",
            2: "Drink",
            4: "Fuel",
            6: "Tool",
            7: "Clothes",
            8: "Shoe",
            11: "Bag",
            12: "Health",
            13: "Happy",
            14: "DrugTimes"
        }
        return [(mapping.get(ia.Int1), ia.Int2) for ia in self.ItemsAttributes]

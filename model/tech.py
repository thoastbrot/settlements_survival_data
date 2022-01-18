# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

from model.common import SingleValues, LocalizedString


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
    TechModule: int  # TODO: how can THIS be optional??
    NeedPoint: int
    PreTechList: PreTech
    UnlockBuffsList: UnlockBuffs
    HintTechList: HintTech
    UnlockBuildingsList: UnlockBuildings
    Position: Optional[Position]
    TechDescribeList: List[TechDescribe]

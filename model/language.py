# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json


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

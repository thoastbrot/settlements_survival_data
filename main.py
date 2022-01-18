# -*- coding: utf-8 -*-
import json
from typing import Type

import bs4
from dataclasses_json import DataClassJsonMixin
from typing_inspect import get_origin, get_args

from model.buildings import TonwBuilding, Building, LogBuilding
from model.common import SingleValues, LocalizedString
from model.items import ItemType, Item
from model.language import LangConfig
from model.resources import ResourceAttributes, Seed, Animal
from model.tech import Technology, TechnologyModule

# a little ugly, used as global lookup table
language_dict = {}


def build_object(b: bs4.Tag, clazz: DataClassJsonMixin):
    data = build_object_dict(b, clazz)
    return clazz.from_dict(data)


def build_object_dict(b: bs4.Tag, clazz):
    if not b:
        return
    c = {}
    typeval: Type
    for prop, typeval in clazz.__annotations__.items():
        # TODO: find a better way than marking everything optional or subclass, like "or typeval in model"
        if "GenericAlias" in str(typeval.__class__):
            origin = get_origin(typeval)
            if origin == list:
                arg_class = get_args(typeval)
                arg_class = arg_class[0]
                data = []
                if arg_class in (int, str, float):
                    node = b.find(prop)
                    if node:
                        data = [arg_class(val) for val in node.text.split("|")]
                else:
                    for bb in b.findAll(arg_class.__name__):
                        data.append(build_object_dict(bb, arg_class))
            else:
                data = build_object_dict(b.find(prop), typeval.__args__[0])
        elif issubclass(typeval, SingleValues):
            data = []
            for bb in b.findAll(typeval.__name__):
                data.append(typeval.__annotations__["values"](bb.text))
        elif typeval == LocalizedString:
            node = b.find(prop)
            data = str(node.text) if node else None
            data = language_dict.get(data, data)
        else:
            node = b.find(prop)
            data = typeval(node.text) if node else None
        c[prop] = data
    return c


def main():
    # XML files from the game, feel free to enter the full path here.
    language = "English"
    game_files = "data/raw/zipConfig"
    things = {
        "lang": {
            "path": f"{game_files}/Lang.xml",
            "class": LangConfig,
            "element_name": "LangConfig"
        },
        "items": {
            "path": f"{game_files}/Items.xml",
            "class": Item,
            "element_name": "ItemsConfig"
        },
        "itemtypes": {
            "path": f"{game_files}/ItemType.xml",
            "class": ItemType,
            "element_name": "ItemTypeConfig"
        },
        "buildings": {
            "path": f"{game_files}/Building.xml",
            "class": Building,
            "element_name": "BuildingConfig"
        },
        "technologymodules": {
            "path": f"{game_files}/TechnologyModule.xml",
            "class": TechnologyModule,
            "element_name": "TechnologyModuleConfig"
        },
        "technologies": {
            "path": f"{game_files}/Technology.xml",
            "class": Technology,
            "element_name": "TechnologyConfig"
        },
        "commonset_townbuildings": {
            "path": f"{game_files}/CommonSet.xml",
            "class": TonwBuilding,
            "element_name": "TonwBuilding"
        },
        "commonset_logbuildings": {
            "path": f"{game_files}/CommonSet.xml",
            "class": LogBuilding,
            "element_name": "LogBuilding"
        },
        "seeds": {
            "path": f"{game_files}/ResSeed.xml",
            "class": Seed,
            "element_name": "ResSeedConfig"
        },
        "resource_attributes": {
            "path": f"{game_files}/ResAttribute.xml",
            "class": ResourceAttributes,
            "element_name": "ResAttributeConfig"
        },
        "animals": {
            "path": f"{game_files}/Animal.xml",
            "class": Animal,
            "element_name": "AnimalConfig"
        },
    }

    data_dictionary = {}
    global language_dict

    for thing_name, thing in things.items():
        data_dictionary[thing_name] = []
        xb = bs4.BeautifulSoup(open(thing["path"], "r", encoding="utf-8"), features="lxml-xml")
        b_: bs4.Tag
        for b_ in xb.findAll(thing["element_name"]):
            data_dictionary[thing_name].append(build_object(b_, thing["class"]))

        with open(f"./out/{thing_name}.json", "w") as fd:
            print(thing_name)
            if thing_name == "lang":
                language_dict = {obj.ID: obj.get_by_language(language)[0].LangValue for obj in
                                 data_dictionary[thing_name]}
                # continue
                data = language_dict

            else:
                if "ID" in thing["class"].__annotations__:
                    data = {obj.ID: obj.to_dict() for obj in data_dictionary[thing_name]}
                else:
                    data = [obj.to_dict() for obj in data_dictionary[thing_name]]

            json.dump(data, fd, indent=2)


if __name__ == '__main__':
    main()

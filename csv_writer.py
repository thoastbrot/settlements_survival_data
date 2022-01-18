# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from csv import DictWriter
from typing import Dict

from model.buildings import Building, ConsumeAddAbility, Goods, ConsumMaterials
from model.items import Item
from model.resources import ResourceAttributes, FinishRes, Produce
from wiki import get_seed, get_resource_attributes, get_item, get_animal, get_itemtype

with open("out/items.json") as fd:
    items: Dict = json.load(fd)
with open("out/itemtypes.json") as fd:
    itemtypes: Dict = json.load(fd)
with open("out/buildings.json") as fd:
    buildings: Dict = json.load(fd)
with open("out/seeds.json") as fd:
    seeds: Dict = json.load(fd)
with open("out/resource_attributes.json") as fd:
    resource_attributes: Dict = json.load(fd)


def rate_my_recipe(consume_ability: ConsumeAddAbility) -> (float, int, int):
    cost = 0
    production = 0

    seed = get_seed(consume_ability.SeedId) if consume_ability.SeedId else None
    # both crop and tree have NumRes
    if seed:
        for harvest in get_resource_attributes(seed.ResID).FinishResList:
            item: Item = Item.from_dict(items.get(str(harvest.ID)))
            production += item.Worth * harvest.NumRange.avg()

    cm: ConsumMaterials
    for cm in consume_ability.ConsumMaterialsList:
        item: Item = Item.from_dict(items.get(str(cm.ID)))
        cost += item.Worth * cm.Num

    om: Goods
    for om in consume_ability.ProduceType:
        item: Item = Item.from_dict(items.get(str(om.ID)))
        production += item.Worth * om.Educated

    return round(production / (cost if cost > 0 else 1), 2), cost, production


def generate_recipes():
    fields = ["Name", "Qty", "Value", "Time", "Ingredients", "Workers", "Building", "Rating", "Category"]
    ingredient_sep = ", "

    recipes = defaultdict(list)
    for building in buildings.values():
        building = Building.from_dict(building)
        if building.Name == "not used":
            continue
        consume_ability: ConsumeAddAbility
        for consume_ability in building.ConsumeAddAbilityList:
            seed = get_seed(consume_ability.SeedId) if consume_ability.SeedId else None
            if seed:
                seed_attrs: ResourceAttributes = get_resource_attributes(seed.ResID)
                if seed_attrs.EntityTypeName == "crop":
                    produce: FinishRes
                    for produce in seed_attrs.FinishResList:
                        item = get_item(produce.ID)
                        recipe_row = {
                            "Name": item.Name,
                            "Qty": produce.NumRange.avg(),
                            "Value": ", ".join(["{1} x {0}".format(*i) for i in item.ItemAttributesWithName]),
                            "Time": 1,
                            "Ingredients": "",
                            "Workers": 1,
                            "Building": building.Name,
                            "Rating": rate_my_recipe(consume_ability)[0],
                            "Category": " / ".join([get_itemtype(type_id).Name for type_id in item.TypeList])
                        }
                        recipes[produce.ID].append(recipe_row)
                elif seed_attrs.EntityTypeName in ["tree", "fruitTree"]:
                    item = get_item(seed_attrs.FruitID)
                    recipe_row = {
                        "Name": item.Name,
                        "Qty": seed_attrs.NumRange.avg(),
                        "Value": ", ".join(["{1} x {0}".format(*i) for i in item.ItemAttributesWithName]),
                        "Time": 1,
                        "Ingredients": "",
                        "Workers": 1,
                        "Building": building.Name,
                        "Rating": rate_my_recipe(consume_ability)[0],
                        "Category": " / ".join([get_itemtype(type_id).Name for type_id in item.TypeList])}
                    recipes[seed_attrs.FruitID].append(recipe_row)
                else:
                    raise NotImplementedError("missing a seed type")

            produce: Goods
            for produce in consume_ability.ProduceType:
                item = get_item(produce.ID)
                recipe_row = {
                    "Name": item.Name,
                    "Qty": produce.Educated,
                    "Value": ", ".join(["{1} x {0}".format(*i) for i in item.ItemAttributesWithName]),
                    "Time": 1,
                    "Ingredients": ingredient_sep.join([f"{c.Num}x {Item.from_dict(items.get(str(c.ID))).Name}" for c in
                                                        consume_ability.ConsumMaterialsList]),
                    "Workers": 1,
                    "Building": building.Name,
                    "Rating": rate_my_recipe(consume_ability)[0],
                    "Category": " / ".join([get_itemtype(type_id).Name for type_id in item.TypeList])
                }
                recipes[produce.ID].append(recipe_row)
        for animal_id in building.CanKeepAnimalList:
            animal = get_animal(animal_id)
            animal_attrs: ResourceAttributes = get_resource_attributes(animal.ResID)
            animal_produce: Produce

            for animal_produce in animal.ProduceList:
                # print(f"{get_item(animal_produce.ID).Name} x {animal_produce.NumRange}")
                item = get_item(animal_produce.ID)
                r = {
                    "Name": item.Name,
                    "Qty": str(animal_produce.NumRange),
                    "Value": ", ".join(["{1} x {0}".format(*i) for i in item.ItemAttributesWithName]),
                    "Time": 1,
                    "Ingredients": f"1x {animal.Name}",
                    "Workers": 1,
                    "Building": building.Name,
                    "Rating": animal_produce.NumRange.avg(),
                    "Category": " / ".join([get_itemtype(type_id).Name for type_id in item.TypeList])
                }
                # print(animal.ID, items.get(str(animal.ID)).get("Name"))
                recipes[animal.ID].append(r)

    # for k in recipes:
    # print(k)
    # print(best_recipe(recipes[k]))

    with open("out/items.csv", "w", newline="") as fd:
        dw = DictWriter(fd, fieldnames=fields, dialect="excel")
        dw.writeheader()
        for k in recipes.values():
            for k_ in k:
                dw.writerow(k_)
            # dw.writerow(best_recipe(k))


def best_recipe(item_recipes):
    return sorted(item_recipes, key=lambda d: d["Rating"])[-1]


if __name__ == '__main__':
    generate_recipes()

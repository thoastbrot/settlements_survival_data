import json
import logging
import re
from collections import defaultdict
from string import Template
from typing import Optional, List, Dict

from model.buildings import ConsumeAddAbility, Building
from model.items import Item, ItemType
from model.resources import Seed, ResourceAttributes, Animal
from model.tech import TechnologyModule, Technology

building_sidebar_tpl = Template("""
===${Name}===
{{SetSurBuilding|image=[[File:SetSur ${Icon}.png|200px|${Name}]]
|id=${ID}
|cost=${cost}
|size=$size
|maxWorkers=${maxWorkers}
|inputItems=
|outputItems=
|builders=2
|tech=$tech
}}
$description
$recipes
{{-}}
""")

with open("out/buildings.json") as fd:
    buildings: Dict = json.load(fd)
with open("out/lang.json") as fd:
    language: Dict = json.load(fd)
with open("out/items.json") as fd:
    items: Dict = json.load(fd)
with open("out/itemtypes.json") as fd:
    itemtypes: Dict = json.load(fd)
with open("out/technologies.json") as fd:
    technologies: Dict = json.load(fd)
with open("out/technologymodules.json") as fd:
    technologymodules: Dict = json.load(fd)
with open("out/commonset_townbuildings.json") as fd:
    commonset_townbuildings: List[Dict] = json.load(fd)
with open("out/commonset_logbuildings.json") as fd:
    commonset_logbuildings: List[Dict] = json.load(fd)
with open("out/seeds.json") as fd:
    seeds: Dict = json.load(fd)
with open("out/animals.json") as fd:
    animals: Dict = json.load(fd)
with open("out/resource_attributes.json") as fd:
    resource_attributes: Dict = json.load(fd)


# TODO: mediawiki tables abstraction layer? so ugly to write and read.

def prepare_description(in_str):
    colorless = re \
        .sub(r"<color=#([a-fA-F0-9]+)>", "", in_str) \
        .replace("</color>", "")
    fixed_interpunction = re.sub(r"([,.])([a-zA-Z])", "\g<1> \g<2>", colorless)
    return fixed_interpunction


def wikilink(page_id: int):
    # use the old formatting, skip escaping braces
    return "[[Page#{{{%d|}}}|{{{%d|}}}]]" % (page_id, page_id)


def itemlink(item_id: int, qty: int):
    global language
    # name = language.get(f"Item_Name_{item_id}") or item_id
    item = get_item(item_id)
    # TODO qty can be string for ranges, not intended, but template change required
    # return "{{SetSurRes|%s|%s}}" % (qty, name)
    item_category = "Items (dont)"
    link = f"Settlement Survival/{item_category}#{item.Name}"
    return "[[File:SetSur %s.png|30px|%s|link=%s]] x %s" % (item.Icon, item.Name, link, qty)


def get_tech_to_unlock(building_id: int) -> Optional[Technology]:
    for t in technologies.values():
        if building_id in t.get("UnlockBuildingsList"):
            return Technology.from_dict(t)


def get_item(item_id: int) -> Optional[Item]:
    item = items.get(str(item_id))
    if item:
        return Item.from_dict(item)
    else:
        raise RuntimeError("Item id %s not found" % item_id)


def get_itemtype(itemtype_id: int) -> Optional[ItemType]:
    itemtype = itemtypes.get(str(itemtype_id))
    if itemtype:
        return ItemType.from_dict(itemtype)
    else:
        raise RuntimeError("Itemtype id %s not found" % itemtype_id)


def get_tech(tech_id: int) -> Optional[Technology]:
    tech = technologies.get(str(tech_id))
    if tech:
        return Technology.from_dict(tech)


def get_tech_module(tech_module_id: int) -> Optional[TechnologyModule]:
    tech_module = technologymodules.get(str(tech_module_id))
    if tech_module:
        return TechnologyModule.from_dict(tech_module)


def get_building_category(building_id: int) -> str:
    for t in commonset_logbuildings:
        if building_id in t.get("BuildingID"):
            return t.get("Name")


def get_resource_attributes(res_id: int) -> Optional[ResourceAttributes]:
    res = resource_attributes.get(str(res_id))
    if res:
        return ResourceAttributes.from_dict(res)


def get_seed(seed_id: int) -> Optional[Seed]:
    seed = seeds.get(str(seed_id))
    if seed:
        return Seed.from_dict(seed)


def get_animal(animal_id: int) -> Optional[Animal]:
    animal = animals.get(str(animal_id))
    if animal:
        return Animal.from_dict(animal)


def get_recipes(recipes: List[ConsumeAddAbility]) -> str:
    if not recipes:
        return ""

    by_entity_type = defaultdict(list)
    headings = {
        "crop": [
            'Seed',
            'colspan="2"|Output <small>(uneducated/educated)</small>',
            'colspan="2"|req. temp for survival/growth',
        ],
        "fruitTree": [
            'Seed',
            'colspan="2"|Output <small>(uneducated/educated)</small>',
            'req. temp for output',
            'Days to grow'
        ],
        "tree": [
            'Seed',
            'colspan="2"|Output <small>(uneducated/educated)</small>',
            'req. temp for output',
            'Days to grow'
        ],
        "default_recipe": [
            'Input',
            'colspan="2"|Output <small>(uneducated/educated)</small>',
            'req. technology',
        ]
    }
    for recipe in recipes:
        # animals?
        seed = get_seed(recipe.SeedId) if recipe.SeedId else None
        if seed:
            seed_attrs = get_resource_attributes(seed.ResID)

            # I assume, there is not one building so far ending up with different entity types.
            # but we're following the possibilities of the XML definition, which would allow that.
            if seed_attrs.EntityTypeName == "crop":
                for harvest in seed_attrs.FinishResList:
                    recipe_row = [
                        seed.Name,
                        itemlink(harvest.ID, str(harvest.UnEducatedNumRange)),
                        itemlink(harvest.ID, str(harvest.NumRange)),
                        str(seed_attrs.DeadTmc),
                        str(seed_attrs.GrowTmc),
                    ]
                    by_entity_type[seed_attrs.EntityTypeName].append(recipe_row)
            elif seed_attrs.EntityTypeName in ["tree", "fruitTree"]:

                recipe_row = [
                    seed.Name,
                    itemlink(seed_attrs.FruitID, str(seed_attrs.NumRange)),
                    itemlink(seed_attrs.FruitID, str(seed_attrs.NumRange)),
                    str(seed_attrs.FruitGrowTmc),
                    str(seed_attrs.RipeDays),
                ]
                by_entity_type[seed_attrs.EntityTypeName].append(recipe_row)
                # probably what you get when felling the trees/removing the orchard
                # for harvest in seed_attrs.FinishResList:
                #     recipe_row = [
                #         seed.Name,
                #         itemlink(harvest.ID, str(harvest.UnEducatedNumRange)),
                #         itemlink(harvest.ID, str(harvest.NumRange)),
                #         "-",
                #         str(seed_attrs.RipeDays),
                #     ]
                #     by_entity_type[seed_attrs.EntityTypeName].append(recipe_row)
            else:
                raise NotImplementedError("missing a seed type")
        # regular recipe type
        else:
            tech = get_tech(recipe.UnlockTech) if recipe.UnlockTech else None
            recipe_row = [
                ", ".join([itemlink(i.ID, i.Num) for i in recipe.ConsumMaterialsList]),
                ",".join([itemlink(i.ID, i.UnEducated) for i in recipe.ProduceType]),
                ",".join([itemlink(i.ID, i.Educated) for i in recipe.ProduceType]),
                tech.Name if tech else ""
            ]
            if recipe_row[0] or recipe_row[1]:
                by_entity_type["default_recipe"].append(recipe_row)

    out = "\n"
    for recipe_type, recipes in by_entity_type.items():
        if not recipes:
            continue
        out += "{| class=\"wikitable\"\n"
        out += "!" + "||".join(map(str, headings.get(recipe_type, "other"))) + "\n"
        out += "|-\n"

        for recipe in recipes:
            out += "|" + "||".join(map(str, recipe)) + "\n"
            out += "|-\n"
        out += "|}\n"

    return out


# TODO
def get_animal_products(animals: List[int]) -> str:
    animals: List[Animal] = [get_animal(i) for i in animals]
    if not animals:
        return ""

    headings = {}
    out = "\n"
    out += "{| class=\"wikitable\"\n"
    out += "!" + "||".join(map(str, headings.get(recipe_type, "other"))) + "\n"
    out += "|-\n"
    for animal in animals:
        out += "|" + "||".join(map(str, recipe)) + "\n"
        out += "|-\n"

    return out


def generate_buildings():
    categories = {}

    for building in buildings.values():
        building = Building.from_dict(building)
        if building.Name == "not used":
            continue

        # TODO: remove in favor of separate table
        inputItems = []
        outputItems = []
        ability: ConsumeAddAbility
        for ability in building.ConsumeAddAbilityList:
            for material in ability.ConsumMaterialsList:
                inputItems.append(itemlink(material.ID, material.Num))
            for material in ability.ProduceType:
                outputItems.append(itemlink(material.ID, material.UnEducated))

        tech = get_tech_to_unlock(building.ID)
        category = get_building_category(building.ID)
        if not category:
            logging.error("didn't write %s (%s) as it has no category", building.Name, building.ID)
            continue

        if tech:
            tech_module = get_tech_module(tech.TechModule)
            if tech_module:
                pretech = [get_tech(p).Name for p in tech.PreTechList]
                tech_tree = " > ".join([category, *pretech, tech.Name])
            else:
                tech_tree = tech.Name
        else:
            tech_tree = ""

        # precalculations
        if building.AllConsumResList:
            cost = [itemlink(i.ID, i.Num) for i in building.AllConsumResList]
            cost = ", ".join(cost)
        elif building.MeshConsumeResList:
            cost = [itemlink(i.ID, i.Num) for i in building.MeshConsumeResList]
            cost = ", ".join(cost) + " per tile"
        else:
            cost = ""
        size = building.FixedSize
        if size:
            rows = size.Attach.strip().split()
            size_xy = f"{len(rows)}x{len(rows[0].split(','))}"
        else:
            size_xy = ""

        recipes = get_recipes(building.ConsumeAddAbilityList)
        # TODO: integrate animal products here?
        text = building_sidebar_tpl.substitute(
            **building.to_dict(),
            cost=cost,
            maxWorkers=building.WorkerRange.Upper if building.WorkerRange else "0",
            inputItems=", ".join(list(set(inputItems))),
            outputItems=", ".join(list(set(outputItems))),
            size=size_xy,
            tech=tech_tree,
            description=prepare_description(building.Des),
            recipes=recipes,
        )
        categories.setdefault(category, []).append(text)

    with open("out/buildings.txt", "w", encoding="utf-8") as wiki_text:
        for c_name, entries in categories.items():
            if c_name == "other":
                continue
            wiki_text.write(f"=={c_name}==\n")
            for entry in entries:
                wiki_text.write(entry)


def get_item_type(item, level):
    if level in (0, 1) and len(item.TypeList) > level:
        return get_itemtype(item.TypeList[level])


def generate_items():
    res = defaultdict(lambda: defaultdict(list))
    for v in map(lambda i: Item.from_dict(i), items.values()):

        maintype = get_item_type(v, 0)
        subtype = get_item_type(v, 1)
        if maintype and subtype:
            res[maintype.Name][subtype.Name].append(v)
        elif maintype:
            res[maintype.Name]["..."].append(v)
        else:
            pass

    base_columns = ["ID", "Icon", "Name", "Sell Price", "Order Price", "Usage Value", "Description"]
    with open("out/wiki_items.txt", "w") as wiki_items:
        for main_itemtype_name, firstlevel in res.items():
            columns = base_columns.copy()
            foobar = list(firstlevel.values())[0]
            has_usage_value = len(foobar[0].ItemAttributesWithName) > 0
            if not has_usage_value:
                columns.remove("Usage Value")
            wiki_items.write(f"== {main_itemtype_name} ==\n")

            wiki_items.write('{| class="wikitable"\n')
            wiki_items.write(f"! {'||'.join(columns)}\n")

            for sub_itemtype_name, item_list in firstlevel.items():

                wiki_items.write("|+\n")
                if sub_itemtype_name != "...":
                    wiki_items.write(f"! colspan={len(columns)} | {sub_itemtype_name} \n")
                    wiki_items.write("|+\n")

                for item in item_list:
                    # not in the game
                    if "rat" in item.Name.lower():
                        continue
                    icon = "[[File:SetSur %s.png|30px|%s]]" % (item.Icon, item.Name)
                    if has_usage_value:
                        usage_value = ", ".join([str(i[1]) for i in item.ItemAttributesWithName])
                        row = [item.ID, icon, item.Name, item.Worth, item.OrderWorth, usage_value, prepare_description(item.Des)]
                    else:
                        row = [item.ID, icon, item.Name, item.Worth, item.OrderWorth, prepare_description(item.Des)]
                    wiki_items.write(
                        f"| {'||'.join(map(str, row))}\n")
                    wiki_items.write("|+\n")
            wiki_items.write("|}\n")


if __name__ == '__main__':
    generate_items()
    # generate_buildings()

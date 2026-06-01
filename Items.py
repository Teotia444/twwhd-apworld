from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple, Optional
import pymem

from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from worlds.AutoWorld import World
if TYPE_CHECKING:
    from .randomizers.Dungeons import Dungeon

def item_factory(items: str | Iterable[str], world: World) -> Item | list[Item]:
    """
    Create items based on their names.
    Depending on the input, this function can return a single item or a list of items.

    :param items: The name or names of the items to create.
    :param world: The game world.
    :raises KeyError: If an unknown item name is provided.
    :return: A single item or a list of items.
    """
    ret: list[Item] = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in ITEM_TABLE:
            ret.append(world.create_item(item))
        else:
            raise KeyError(f"Unknown item {item}")

    return ret[0] if singleton else ret




class TWWHDItemData(NamedTuple):
    """
    This class represents the data for an item in The Wind Waker HD.

    :param type: The type of the item (e.g., "Item", "Dungeon Item").
    :param classification: The item's classification (progression, useful, filler).
    :param code: The unique code identifier for the item.
    :param quantity: The number of this item available.
    :param item_id: The ID used to represent the item in-game.
    """

    type: str
    classification: IC
    code: Optional[int]
    quantity: int
    item_id: Optional[int]

class TWWHDItem(Item):
    """
    This class represents an item in The Wind Waker HD.

    :param name: The item's name.
    :param player: The ID of the player who owns the item.
    :param data: The data associated with this item.
    :param classification: Optional classification to override the default.
    """

    game: str = "The Wind Waker HD"
    type: Optional[str]
    dungeon: Optional["Dungeon"] = None

    def __init__(self, name: str, player: int, data: TWWHDItemData, classification: Optional[IC] = None) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else TWWHDItem.get_apid(data.code),
            player,
        )

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 99107105
        return base_id + code

    @property
    def dungeon_item(self) -> Optional[str]:
        """
        Determine if the item is a dungeon item and, if so, returns its type.

        :return: The type of dungeon item, or `None` if it is not a dungeon item.
        """
        if self.type in ("Small Key", "Big Key", "Map", "Compass"):
            return self.type
        return None


ITEM_TABLE: dict[str, TWWHDItemData] = {
    "Telescope":                 TWWHDItemData("Item",      IC.useful,                       0,  1, 0x20),
  # "Boat's Sail":               TWWHDItemData("Item",      IC.progression,                  1,  1, 0x78),  # noqa: E131
    "Wind Waker":                TWWHDItemData("Item",      IC.progression,                  2,  1, 0x22),
    "Grappling Hook":            TWWHDItemData("Item",      IC.progression,                  3,  1, 0x25),
    "Spoils Bag":                TWWHDItemData("Item",      IC.progression,                  4,  1, 0x24),
    "Boomerang":                 TWWHDItemData("Item",      IC.progression,                  5,  1, 0x2D),
    "Deku Leaf":                 TWWHDItemData("Item",      IC.progression,                  6,  1, 0x34),
    "Tingle Bottle":             TWWHDItemData("Item",      IC.filler,                       7,  1, 0x21),
    "Iron Boots":                TWWHDItemData("Item",      IC.progression,                  8,  1, 0x29),
    "Magic Armor":               TWWHDItemData("Item",      IC.progression,                  9,  1, 0x2A),
    "Bait Bag":                  TWWHDItemData("Item",      IC.progression,                 10,  1, 0x2C),
    "Bombs":                     TWWHDItemData("Item",      IC.progression,                 11,  1, 0x31),
    "Delivery Bag":              TWWHDItemData("Item",      IC.progression,                 12,  1, 0x30),
    "Hookshot":                  TWWHDItemData("Item",      IC.progression,                 13,  1, 0x2F),
    "Skull Hammer":              TWWHDItemData("Item",      IC.progression,                 14,  1, 0x33),
    "Power Bracelets":           TWWHDItemData("Item",      IC.progression,                 15,  1, 0x28),

    "Hero's Charm":              TWWHDItemData("Item",      IC.useful,                      16,  1, 0x43),
    "Hurricane Spin":            TWWHDItemData("Item",      IC.useful,                      17,  1, 0xAA),
    "Dragon Tingle Statue":      TWWHDItemData("Item",      IC.progression,                 18,  1, 0xA3),
    "Forbidden Tingle Statue":   TWWHDItemData("Item",      IC.progression,                 19,  1, 0xA4),
    "Goddess Tingle Statue":     TWWHDItemData("Item",      IC.progression,                 20,  1, 0xA5),
    "Earth Tingle Statue":       TWWHDItemData("Item",      IC.progression,                 21,  1, 0xA6),
    "Wind Tingle Statue":        TWWHDItemData("Item",      IC.progression,                 22,  1, 0xA7),

    "Wind's Requiem":            TWWHDItemData("Item",      IC.progression,                 23,  1, 0x6D),
    "Ballad of Gales":           TWWHDItemData("Item",      IC.progression,                 24,  1, 0x6E),
    "Command Melody":            TWWHDItemData("Item",      IC.progression,                 25,  1, 0x6F),
    "Earth God's Lyric":         TWWHDItemData("Item",      IC.progression,                 26,  1, 0x70),
    "Wind God's Aria":           TWWHDItemData("Item",      IC.progression,                 27,  1, 0x71),
    "Song of Passing":           TWWHDItemData("Item",      IC.progression,                 28,  1, 0x72),

    "Triforce Shard 1":          TWWHDItemData("Item",      IC.progression,                 29,  1, 0x61),
    "Triforce Shard 2":          TWWHDItemData("Item",      IC.progression,                 30,  1, 0x62),
    "Triforce Shard 3":          TWWHDItemData("Item",      IC.progression,                 31,  1, 0x63),
    "Triforce Shard 4":          TWWHDItemData("Item",      IC.progression,                 32,  1, 0x64),
    "Triforce Shard 5":          TWWHDItemData("Item",      IC.progression,                 33,  1, 0x65),
    "Triforce Shard 6":          TWWHDItemData("Item",      IC.progression,                 34,  1, 0x66),
    "Triforce Shard 7":          TWWHDItemData("Item",      IC.progression,                 35,  1, 0x67),
    "Triforce Shard 8":          TWWHDItemData("Item",      IC.progression,                 36,  1, 0x68),

    "Skull Necklace":            TWWHDItemData("Item",      IC.filler,                      37,  9, 0x45),
    "Boko Baba Seed":            TWWHDItemData("Item",      IC.filler,                      38,  1, 0x46),
    "Golden Feather":            TWWHDItemData("Item",      IC.filler,                      39,  9, 0x47),
    "Knights Crest":             TWWHDItemData("Item",      IC.filler,                      40,  3, 0x48),
    "Red Chu Jelly":             TWWHDItemData("Item",      IC.filler,                      41,  1, 0x49),
    "Green Chu Jelly":           TWWHDItemData("Item",      IC.filler,                      42,  1, 0x4A),
    "Joy Pendant":               TWWHDItemData("Item",      IC.filler,                      43, 20, 0x1F),
    "All Purpose Bait":          TWWHDItemData("Item",      IC.filler,                      44,  1, 0x82),
    "Hyoi Pear":                 TWWHDItemData("Item",      IC.filler,                      45,  4, 0x83),

    "Note to Mom":               TWWHDItemData("Item",      IC.progression,                 46,  1, 0x99),
    "Maggie's Letter":           TWWHDItemData("Item",      IC.progression,                 47,  1, 0x9A),
    "Moblin's Letter":           TWWHDItemData("Item",      IC.progression,                 48,  1, 0x9B),
    "Cabana Deed":               TWWHDItemData("Item",      IC.progression,                 49,  1, 0x9C),
    "Fill Up Coupon":            TWWHDItemData("Item",      IC.useful,                      50,  1, 0x9E),

    "Nayru's Pearl":             TWWHDItemData("Item",      IC.progression,                 51,  1, 0x69),
    "Din's Pearl":               TWWHDItemData("Item",      IC.progression,                 52,  1, 0x6A),
    "Farore's Pearl":            TWWHDItemData("Item",      IC.progression,                 53,  1, 0x6B),

    "Progressive Sword":         TWWHDItemData("Item",      IC.progression,                 54,  4, 0x38),
    "Progressive Shield":        TWWHDItemData("Item",      IC.progression,                 55,  2, 0x3B),
    "Progressive Picto Box":     TWWHDItemData("Item",      IC.progression,                 56,  2, 0x23),
    "Progressive Bow":           TWWHDItemData("Item",      IC.progression,                 57,  3, 0x27),
    "Progressive Magic Meter":   TWWHDItemData("Item",      IC.progression,                 58,  2, 0xB1),
    "Progressive Quiver":        TWWHDItemData("Item",      IC.progression,                 59,  2, 0xAF),
    "Progressive Bomb Bag":      TWWHDItemData("Item",      IC.useful,                      60,  2, 0xAD),
    "Progressive Wallet":        TWWHDItemData("Item",      IC.progression,                 61,  2, 0xAB),
    "Empty Bottle":              TWWHDItemData("Item",      IC.progression,                 62,  4, 0x50),

    "Triforce Chart 1":          TWWHDItemData("Item",      IC.progression_skip_balancing,  63,  1, 0xFE),
    "Triforce Chart 2":          TWWHDItemData("Item",      IC.progression_skip_balancing,  64,  1, 0xFD),
    "Triforce Chart 3":          TWWHDItemData("Item",      IC.progression_skip_balancing,  65,  1, 0xFC),
    "Treasure Chart 1":          TWWHDItemData("Item",      IC.progression_skip_balancing,  71,  1, 0xE7),
    "Treasure Chart 2":          TWWHDItemData("Item",      IC.progression_skip_balancing,  72,  1, 0xEE),
    "Treasure Chart 3":          TWWHDItemData("Item",      IC.progression_skip_balancing,  73,  1, 0xE0),
    "Treasure Chart 4":          TWWHDItemData("Item",      IC.progression_skip_balancing,  74,  1, 0xE1),
    "Treasure Chart 5":          TWWHDItemData("Item",      IC.progression_skip_balancing,  75,  1, 0xF2),
    "Treasure Chart 6":          TWWHDItemData("Item",      IC.progression_skip_balancing,  76,  1, 0xEA),
    "Treasure Chart 7":          TWWHDItemData("Item",      IC.progression_skip_balancing,  77,  1, 0xCC),
    "Treasure Chart 8":          TWWHDItemData("Item",      IC.progression_skip_balancing,  78,  1, 0xD4),
    "Treasure Chart 9":          TWWHDItemData("Item",      IC.progression_skip_balancing,  79,  1, 0xDA),
    "Treasure Chart 10":         TWWHDItemData("Item",      IC.progression_skip_balancing,  80,  1, 0xDE),
    "Treasure Chart 11":         TWWHDItemData("Item",      IC.progression_skip_balancing,  81,  1, 0xF6),
    "Treasure Chart 12":         TWWHDItemData("Item",      IC.progression_skip_balancing,  82,  1, 0xE9),
    "Treasure Chart 13":         TWWHDItemData("Item",      IC.progression_skip_balancing,  83,  1, 0xCF),
    "Treasure Chart 14":         TWWHDItemData("Item",      IC.progression_skip_balancing,  84,  1, 0xDD),
    "Treasure Chart 15":         TWWHDItemData("Item",      IC.progression_skip_balancing,  85,  1, 0xF5),
    "Treasure Chart 16":         TWWHDItemData("Item",      IC.progression_skip_balancing,  86,  1, 0xE3),
    "Treasure Chart 17":         TWWHDItemData("Item",      IC.progression_skip_balancing,  87,  1, 0xD7),
    "Treasure Chart 18":         TWWHDItemData("Item",      IC.progression_skip_balancing,  88,  1, 0xE4),
    "Treasure Chart 19":         TWWHDItemData("Item",      IC.progression_skip_balancing,  89,  1, 0xD1),
    "Treasure Chart 20":         TWWHDItemData("Item",      IC.progression_skip_balancing,  90,  1, 0xF3),
    "Treasure Chart 21":         TWWHDItemData("Item",      IC.progression_skip_balancing,  91,  1, 0xCE),
    "Treasure Chart 22":         TWWHDItemData("Item",      IC.progression_skip_balancing,  92,  1, 0xD9),
    "Treasure Chart 23":         TWWHDItemData("Item",      IC.progression_skip_balancing,  93,  1, 0xF1),
    "Treasure Chart 24":         TWWHDItemData("Item",      IC.progression_skip_balancing,  94,  1, 0xEB),
    "Treasure Chart 25":         TWWHDItemData("Item",      IC.progression_skip_balancing,  95,  1, 0xD6),
    "Treasure Chart 26":         TWWHDItemData("Item",      IC.progression_skip_balancing,  96,  1, 0xD3),
    "Treasure Chart 27":         TWWHDItemData("Item",      IC.progression_skip_balancing,  97,  1, 0xCD),
    "Treasure Chart 28":         TWWHDItemData("Item",      IC.progression_skip_balancing,  98,  1, 0xE2),
    "Treasure Chart 29":         TWWHDItemData("Item",      IC.progression_skip_balancing,  99,  1, 0xE6),
    "Treasure Chart 30":         TWWHDItemData("Item",      IC.progression_skip_balancing, 100,  1, 0xF4),
    "Treasure Chart 31":         TWWHDItemData("Item",      IC.progression_skip_balancing, 101,  1, 0xF0),
    "Treasure Chart 32":         TWWHDItemData("Item",      IC.progression_skip_balancing, 102,  1, 0xD0),
    "Treasure Chart 33":         TWWHDItemData("Item",      IC.progression_skip_balancing, 103,  1, 0xEF),
    "Treasure Chart 34":         TWWHDItemData("Item",      IC.progression_skip_balancing, 104,  1, 0xE5),
    "Treasure Chart 35":         TWWHDItemData("Item",      IC.progression_skip_balancing, 105,  1, 0xE8),
    "Treasure Chart 36":         TWWHDItemData("Item",      IC.progression_skip_balancing, 106,  1, 0xD8),
    "Treasure Chart 37":         TWWHDItemData("Item",      IC.progression_skip_balancing, 107,  1, 0xD5),
    "Treasure Chart 38":         TWWHDItemData("Item",      IC.progression_skip_balancing, 108,  1, 0xED),
    "Treasure Chart 39":         TWWHDItemData("Item",      IC.progression_skip_balancing, 109,  1, 0xEC),
    "Treasure Chart 40":         TWWHDItemData("Item",      IC.progression_skip_balancing, 110,  1, 0xDF),
    "Treasure Chart 41":         TWWHDItemData("Item",      IC.progression_skip_balancing, 111,  1, 0xD2),

    "Tingle's Chart":            TWWHDItemData("Item",      IC.filler,                     112,  1, 0xDC),
    "Ghost Ship Chart":          TWWHDItemData("Item",      IC.progression,                113,  1, 0xDB),
    "Octo Chart":                TWWHDItemData("Item",      IC.filler,                     114,  1, 0xCA),
    "Great Fairy Chart":         TWWHDItemData("Item",      IC.filler,                     115,  1, 0xC9),
    "Secret Cave Chart":         TWWHDItemData("Item",      IC.filler,                     116,  1, 0xC6),
    "Light Ring Chart":          TWWHDItemData("Item",      IC.filler,                     117,  1, 0xC5),
    "Platform Chart":            TWWHDItemData("Item",      IC.filler,                     118,  1, 0xC4),
    "Beedle's Chart":            TWWHDItemData("Item",      IC.filler,                     119,  1, 0xC3),
    "Submarine Chart":           TWWHDItemData("Item",      IC.filler,                     120,  1, 0xC2),

    "Green Rupee":               TWWHDItemData("Item",      IC.filler,                     121,  1, 0x01),
    "Blue Rupee":                TWWHDItemData("Item",      IC.filler,                     122,  2, 0x02),
    "Yellow Rupee":              TWWHDItemData("Item",      IC.filler,                     123,  3, 0x03),
    "Red Rupee":                 TWWHDItemData("Item",      IC.filler,                     124,  8, 0x04),
    "Purple Rupee":              TWWHDItemData("Item",      IC.filler,                     125, 90, 0x05),
    "Orange Rupee":              TWWHDItemData("Item",      IC.useful,                     126, 15, 0x06),
    "Silver Rupee":              TWWHDItemData("Item",      IC.useful,                     127, 20, 0x0F),
    "Rainbow Rupee":             TWWHDItemData("Item",      IC.useful,                     128,  1, 0xB8),

    "Piece of Heart":            TWWHDItemData("Item",      IC.useful,                     129, 44, 0x07),
    "Heart Container":           TWWHDItemData("Item",      IC.useful,                     130,  6, 0x08),

    "Dragon Roost Cavern Big Key":     TWWHDItemData("Big Key",   IC.progression,                131,  1, 0x41),
    "Dragon Roost Cavern Small Key":   TWWHDItemData("Small Key", IC.progression,                132,  4, 0x40),
    "Forbidden Woods Big Key":         TWWHDItemData("Big Key",   IC.progression,                133,  1, 0x5D),
    "Forbidden Woods Small Key":       TWWHDItemData("Small Key", IC.progression,                134,  1, 0x5C),
    "Tower of the Gods Big Key":       TWWHDItemData("Big Key",   IC.progression,                135,  1, 0x73),
    "Tower of the Gods Small Key":     TWWHDItemData("Small Key", IC.progression,                136,  2, 0x60),
    "Earth Temple Big Key":            TWWHDItemData("Big Key",   IC.progression,                138,  1, 0x85),
    "Earth Temple Small Key":          TWWHDItemData("Small Key", IC.progression,                139,  3, 0x84),
    "Wind Temple Big Key":             TWWHDItemData("Big Key",   IC.progression,                140,  1, 0x89),
    "Wind Temple Small Key":           TWWHDItemData("Small Key", IC.progression,                141,  2, 0x88),
    "Dragon Roost Cavern Dungeon Map": TWWHDItemData("Map",       IC.filler,                     142,  1, 0x5A),
    "Dragon Roost Cavern Compass":     TWWHDItemData("Compass",   IC.filler,                     143,  1, 0x5B),
    "Forbidden Woods Dungeon Map":     TWWHDItemData("Map",       IC.filler,                     144,  1, 0x5F),
    "Forbidden Woods Compass":         TWWHDItemData("Compass",   IC.filler,                     145,  1, 0x5E),
    "Tower of the Gods Dungeon Map":   TWWHDItemData("Map",       IC.filler,                     146,  1, 0x74),
    "Tower of the Gods Compass":       TWWHDItemData("Compass",   IC.filler,                     147,  1, 0x75),
    "Forsaken Fortress Dungeon Map":   TWWHDItemData("Map",       IC.filler,                     148,  1, 0x76),
    "Forsaken Fortress Compass":       TWWHDItemData("Compass",   IC.filler,                     149,  1, 0x81),
    "Earth Temple Dungeon Map":        TWWHDItemData("Map",       IC.filler,                     150,  1, 0x86),
    "Earth Temple Compass":            TWWHDItemData("Compass",   IC.filler,                     151,  1, 0x87),
    "Wind Temple Dungeon Map":         TWWHDItemData("Map",       IC.filler,                     152,  1, 0x8A),
    "Wind Temple Compass":             TWWHDItemData("Compass",   IC.filler,                     153,  1, 0x8B),

    "Victory":                         TWWHDItemData("Event",     IC.progression,               None,  1, None),
}

#TODO: add missing treasure charts
ISLAND_NUMBER_TO_CHART_NAME = {
    1: "Treasure Chart 25",
    2: "Treasure Chart 7",
    3: "Treasure Chart 24",
    4: "Triforce Chart 2",
    5: "Treasure Chart 11",
    6: "Green Rupee",
    7: "Treasure Chart 13",
    8: "Treasure Chart 41",
    9: "Treasure Chart 29",
    10: "Treasure Chart 22",
    11: "Treasure Chart 18",
    12: "Treasure Chart 30",
    13: "Treasure Chart 39",
    14: "Treasure Chart 19",
    15: "Treasure Chart 8",
    16: "Treasure Chart 2",
    17: "Treasure Chart 10",
    18: "Treasure Chart 26",
    19: "Treasure Chart 3",
    20: "Treasure Chart 37",
    21: "Treasure Chart 27",
    22: "Treasure Chart 38",
    23: "Triforce Chart 1",
    24: "Treasure Chart 21",
    25: "Treasure Chart 6",
    26: "Treasure Chart 14",
    27: "Treasure Chart 34",
    28: "Treasure Chart 5",
    29: "Treasure Chart 28",
    30: "Treasure Chart 35",
    31: "Triforce Chart 3",
    32: "Green Rupee",
    33: "Treasure Chart 1",
    34: "Treasure Chart 20",
    35: "Treasure Chart 36",
    36: "Treasure Chart 23",
    37: "Treasure Chart 12",
    38: "Treasure Chart 16",
    39: "Treasure Chart 4",
    40: "Treasure Chart 17",
    41: "Treasure Chart 31",
    42: "Green Rupee",
    43: "Treasure Chart 9",
    44: "Green Rupee",
    45: "Treasure Chart 40",
    46: "Green Rupee",
    47: "Treasure Chart 15",
    48: "Treasure Chart 32",
    49: "Treasure Chart 33",
}


LOOKUP_ID_TO_NAME: dict[int, str] = {
    TWWHDItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}

item_name_groups = {
    "Songs": {
        "Wind's Requiem",
        "Ballad of Gales",
        "Command Melody",
        "Earth God's Lyric",
        "Wind God's Aria",
        "Song of Passing",
    },
    "Mail": {
        "Note to Mom",
        "Maggie's Letter",
        "Moblin's Letter",
    },
    "Special Charts": {
        "Tingle's Chart",
        "Ghost Ship Chart",
        "Octo Chart",
        "Great Fairy Chart",
        "Secret Cave Chart",
        "Light Ring Chart",
        "Platform Chart",
        "Beedle's Chart",
        "Submarine Chart",
    },
}
# generic groups, (Name, substring)
_simple_groups = {
    ("Tingle Statues", "Tingle Statue"),
    ("Shards", "Shard"),
    ("Pearls", "Pearl"),
    ("Triforce Charts", "Triforce Chart"),
    ("Treasure Charts", "Treasure Chart"),
    ("Small Keys", "Small Key"),
    ("Big Keys", "Big Key"),
    ("Rupees", "Rupee"),
    ("Dungeon Items", "Compass"),
    ("Dungeon Items", "Map"),
}
for basename, substring in _simple_groups:
    if basename not in item_name_groups:
        item_name_groups[basename] = set()
    for itemname in ITEM_TABLE:
        if substring in itemname:
            item_name_groups[basename].add(itemname)

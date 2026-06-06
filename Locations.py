from enum import Enum, Flag, auto
from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import Location, Region
if TYPE_CHECKING:
    from .randomizers.Dungeons import Dungeon

class TWWHDFlag(Flag):
    """
    This class represents flags used for categorizing game locations.
    Flags are used to group locations by their specific gameplay or logic attributes.
    """

    ALWAYS = auto()
    DUNGEON = auto()
    TNGL_CT = auto()
    DG_SCRT = auto()
    PZL_CVE = auto()
    CBT_CVE = auto()
    SAVAGE = auto()
    GRT_FRY = auto()
    SHRT_SQ = auto()
    LONG_SQ = auto()
    SPOILS = auto()
    MINIGME = auto()
    SPLOOSH = auto()
    FREE_GF = auto()
    MAILBOX = auto()
    PLTFRMS = auto()
    SUBMRIN = auto()
    EYE_RFS = auto()
    BG_OCTO = auto()
    TRI_CHT = auto()
    TRE_CHT = auto()
    XPENSVE = auto()
    ISLND_P = auto()
    MISCELL = auto()
    BOSS = auto()
    OTHER = auto()

class TWWHDLocationType(Enum):
    """
    This class defines constants for various types of locations in The Wind Waker.
    """

    CHART = auto()
    BOCTO = auto()
    CHEST = auto()
    SWTCH = auto()
    PCKUP = auto()
    EVENT = auto()
    SPECL = auto()

class TWWHDLocationData(NamedTuple):
    """
    This class represents the data for a location in The Wind Waker.

    :param code: The unique code identifier for the location.
    :param flags: The flags that categorize the location.
    :param region: The name of the region where the location resides.
    :param stage_id: The stage where the location resides.
    :param type: The type of the location.
    :param bit: The bit in memory that is associated with the location. This is combined with other location data to
    determine where in memory to determine whether the location has been checked. If the location is a special type,
    this bit is ignored.
    :param address: For certain location types, this variable contains the address of the byte with the check bit for
    that location. Defaults to `None`.
    """

    code: Optional[int]
    flags: TWWHDFlag
    region: str
    stage_id: int
    type: TWWHDLocationType
    bit: int
    address: Optional[int] = 0

class TWWHDLocation(Location):
    """
    This class represents a location in The Wind Waker.

    :param player: The ID of the player whose world the location is in.
    :param name: The name of the location.
    :param parent: The location's parent region.
    :param data: The data associated with this location.
    """

    game: str = "The Wind Waker"
    dungeon: Optional["Dungeon"] = None

    def __init__(self, player: int, name: str, parent: Region, data: TWWHDLocationData):
        address = None if data.code is None else TWWHDLocation.get_apid(data.code)
        super().__init__(player, name, address=address, parent=parent)

        self.code = data.code
        self.flags = data.flags
        self.region = data.region
        self.stage_id = data.stage_id
        self.type = data.type
        self.bit = data.bit
        self.address = self.address

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given location code.

        :param code: The unique code for the location.
        :return: The computed Archipelago ID.
        """
        base_id: int = 104100
        return base_id + code
    
DUNGEON_NAMES = [
    "Dragon Roost Cavern",
    "Forbidden Woods",
    "Tower of the Gods",
    "Forsaken Fortress",
    "Earth Temple",
    "Wind Temple",
]

LOCATION_TABLE: dict[str, TWWHDLocationData] = {
    # Outset Island
    "Outset Island - Under Link's House": TWWHDLocationData(
        0, TWWHDFlag.MISCELL, "The Great Sea", 0xB, TWWHDLocationType.CHEST, 5
    ),
    "Outset Island - Mesa's House Chest": TWWHDLocationData(
        1, TWWHDFlag.MISCELL, "The Great Sea", 0xB, TWWHDLocationType.CHEST, 4
    ),
    "Outset Island - Orca Give 10 Knight's Crests": TWWHDLocationData(
        2, TWWHDFlag.SPOILS, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 5, 0xb
    ),
    # "Outset Island - Orca - Hit 500 Times": TWWHDLocationData(
    #     3, TWWHDFlag.OTHER, "The Great Sea"
    # ),
    "Outset Island - Great Fairy": TWWHDLocationData(
        4, TWWHDFlag.GRT_FRY, "The Great Sea", 0xC, TWWHDLocationType.EVENT, 4, 0x30
    ),
    "Outset Island - Jabun's Cave Chest": TWWHDLocationData(
        5, TWWHDFlag.ISLND_P, "The Great Sea", 0xB, TWWHDLocationType.CHEST, 6
    ),
    "Outset Island - Dig up Black Soil": TWWHDLocationData(
        6, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.PCKUP, 2
    ),
    "Outset Island - Savage Labyrinth Floor 30": TWWHDLocationData(
        7, TWWHDFlag.SAVAGE, "Savage Labyrinth", 0xD, TWWHDLocationType.CHEST, 11
    ),
    "Outset Island - Savage Labyrinth Floor 50": TWWHDLocationData(
        8, TWWHDFlag.SAVAGE, "Savage Labyrinth", 0xD, TWWHDLocationType.CHEST, 12
    ),

    # Windfall Island
    "Windfall Island - Tingle First Gift": TWWHDLocationData(
        9, TWWHDFlag.FREE_GF, "The Great Sea", 0xB, TWWHDLocationType.SWTCH, 53
    ),
    "Windfall Island - Tingle Second Gift": TWWHDLocationData(
        10, TWWHDFlag.FREE_GF, "The Great Sea", 0xB, TWWHDLocationType.SWTCH, 54
    ),
    "Windfall Island - Windfall Jail Maze Chest": TWWHDLocationData(
        11, TWWHDFlag.ISLND_P, "The Great Sea", 0xB, TWWHDLocationType.CHEST, 0
    ),
    "Windfall Island - Potion Shop 15 Green Chu": TWWHDLocationData(
        12, TWWHDFlag.SPOILS, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 2, 0xd
    ),
    "Windfall Island - Potion Shop 15 Blue Chu": TWWHDLocationData(
        13, TWWHDFlag.SPOILS | TWWHDFlag.LONG_SQ, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 1, 0xd
    ),
    "Windfall Island - Ivan Catch Killer Bees": TWWHDLocationData(
        14, TWWHDFlag.SHRT_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 6, 0x13
    ),
    "Windfall Island - Mrs. Marie Catch Killer Bees": TWWHDLocationData(
        15, TWWHDFlag.SHRT_SQ, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 7, 0x1f
    ),
    "Windfall Island - Mrs. Marie 1 Joy Pendant": TWWHDLocationData(
        16, TWWHDFlag.SPOILS, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 0, 0xc0
    ),
    "Windfall Island - Mrs. Marie 21 Joy Pendant": TWWHDLocationData(
        17, TWWHDFlag.SPOILS, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 3, 0x1C
    ),
    "Windfall Island - Mrs. Marie 40 Joy Pendant": TWWHDLocationData(
        18, TWWHDFlag.SPOILS, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 2, 0x1C
    ),
    "Windfall Island - Lenzo House Left Chest": TWWHDLocationData(
        19, TWWHDFlag.SHRT_SQ, "The Great Sea", 0xB, TWWHDLocationType.CHEST, 1
    ),
    "Windfall Island - Lenzo House Right Chest": TWWHDLocationData(
        20, TWWHDFlag.SHRT_SQ, "The Great Sea", 0xB, TWWHDLocationType.CHEST, 2
    ),
    "Windfall Island - Lenzo Become Assistant": TWWHDLocationData(
        21, TWWHDFlag.LONG_SQ, "The Great Sea", 0xB, TWWHDLocationType.SPECL, 0, 0xc4
    ),
    "Windfall Island - Lenzo Bring Forest Firefly": TWWHDLocationData(
        22, TWWHDFlag.LONG_SQ, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 5, 0x69
    ),
    "Windfall Island - House of Wealth Chest": TWWHDLocationData(
        23, TWWHDFlag.MISCELL, "The Great Sea", 0xB, TWWHDLocationType.CHEST, 3
    ),
    "Windfall Island - Maggie's Father Give 20 Skull Necklaces": TWWHDLocationData(
        24, TWWHDFlag.SPOILS, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 4, 0xc5
    ),
    "Windfall Island - Maggie Free Item": TWWHDLocationData(
        25, TWWHDFlag.FREE_GF, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 0, 0x6a
    ),
    "Windfall Island - Maggie Delivery Reward": TWWHDLocationData(
        # TODO: Where is the flag for this location. Using a temporary workaround for now.
        26, TWWHDFlag.SHRT_SQ, "The Great Sea", 0xB, TWWHDLocationType.SPECL, 0
    ),
    "Windfall Island - Cafe Postman Delivery": TWWHDLocationData(
        27, TWWHDFlag.SHRT_SQ, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 1, 0x6a
    ),
    "Windfall Island - Kreeb Light the Lighthouse": TWWHDLocationData(
        28, TWWHDFlag.SHRT_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 5,0x1b
    ),
    "Windfall Island - Transparent Chest": TWWHDLocationData(
        29, TWWHDFlag.SHRT_SQ, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 10
    ),
    "Windfall Island - Tott Teach Rhythm": TWWHDLocationData(
        30, TWWHDFlag.FREE_GF, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 6,0xC
    ),
    "Windfall Island - Pirate Ship Chest": TWWHDLocationData(
        31, TWWHDFlag.MINIGME, "The Great Sea", 0xD, TWWHDLocationType.CHEST, 5
    ),
    "Windfall Island - Auction 5 Rupee": TWWHDLocationData(
        32, TWWHDFlag.XPENSVE | TWWHDFlag.MINIGME, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 7, 0x10
    ),
    "Windfall Island - Auction 40 Rupee": TWWHDLocationData(
        33, TWWHDFlag.XPENSVE | TWWHDFlag.MINIGME, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 0, 0xf
    ),
    "Windfall Island - Auction 60 Rupee": TWWHDLocationData(
        34, TWWHDFlag.XPENSVE | TWWHDFlag.MINIGME, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 6, 0x10
    ),
    "Windfall Island - Auction 80 Rupee": TWWHDLocationData(
        35, TWWHDFlag.XPENSVE | TWWHDFlag.MINIGME, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 5, 0x10
    ),
    "Windfall Island - Zunari Exotic Flower": TWWHDLocationData(
        36, TWWHDFlag.SHRT_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 6, 0x69
    ),
    "Windfall Island - Sam Decorate Island": TWWHDLocationData(
        37, TWWHDFlag.LONG_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 4, 0x1B
    ),
    # "Windfall Island - Kane - Place Shop Guru Statue on Gate": TWWHDLocationData(
    #     38, TWWHDFlag.OTHER, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 4, 0x803C5250
    # ),
    # "Windfall Island - Kane - Place Postman Statue on Gate": TWWHDLocationData(
    #     39, TWWHDFlag.OTHER, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 3, 0x803C5250
    # ),
    # "Windfall Island - Kane - Place Six Flags on Gate": TWWHDLocationData(
    #     40, TWWHDFlag.OTHER, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 2, 0x803C5250
    # ),
    # "Windfall Island - Kane - Place Six Idols on Gate": TWWHDLocationData(
    #     41, TWWHDFlag.OTHER, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 1, 0x803C5250
    # ),
    "Windfall Island - Mila Catch Thief": TWWHDLocationData(
        42, TWWHDFlag.SHRT_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 3, 0xE
    ),
    "Windfall Island - Battle Squid First Prize": TWWHDLocationData(
        43, TWWHDFlag.SPLOOSH, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 0, 0xfe
    ),
    "Windfall Island - Battle Squid Second Prize": TWWHDLocationData(
        44, TWWHDFlag.SPLOOSH, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 1, 0xfe
    ),
    "Windfall Island - Battle Squid Under 20 Prize": TWWHDLocationData(
        45, TWWHDFlag.SPLOOSH, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 2, 0xe
    ),
    "Windfall Island - Pompie & Vera Secret Meeting Photo": TWWHDLocationData(
        46, TWWHDFlag.SHRT_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 2, 0x69
    ),
    "Windfall Island - Kamo Full Moon Picture": TWWHDLocationData(
        47, TWWHDFlag.LONG_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 4, 0x69
    ),
    "Windfall Island - Minenco Miss Windfall Picture": TWWHDLocationData(
        48, TWWHDFlag.SHRT_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 3, 0x69
    ),
    "Windfall Island - Linda and Anton": TWWHDLocationData(
        49, TWWHDFlag.LONG_SQ, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 7, 0x22
    ),

    # Dragon Roost Island
    "Dragon Roost Island - Wind Shrine": TWWHDLocationData(
        50, TWWHDFlag.MISCELL, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 3, 0x27
    ),
    "Dragon Roost Island - Hoskit Give 20 Golden Feathers": TWWHDLocationData(
        51, TWWHDFlag.SPOILS, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 7, 0x21
    ),
    "Dragon Roost Island - Boulder Chest": TWWHDLocationData(
        52, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 8
    ),
    "Dragon Roost Island - Fly Across Platforms Around Island": TWWHDLocationData(
        53, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 9
    ),
    "Dragon Roost Island - Baito Mail Game": TWWHDLocationData(
        54, TWWHDFlag.MINIGME, "The Great Sea", 0xB, TWWHDLocationType.EVENT, 0, 0x27
    ),
    "Dragon Roost Island - Cave Chest": TWWHDLocationData(
        55, TWWHDFlag.CBT_CVE, "Dragon Roost Island Secret Cave", 0xD, TWWHDLocationType.CHEST, 0
    ),

    # Dragon Roost Cavern
    "Dragon Roost Cavern - First Room Chest": TWWHDLocationData(
        56, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 0
    ),
    "Dragon Roost Cavern - Water Jug Alcove Chest": TWWHDLocationData(
        57, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 2
    ),
    "Dragon Roost Cavern - Water Jug On Upper Shelf": TWWHDLocationData(
        58, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWHDLocationType.PCKUP, 1
    ),
    "Dragon Roost Cavern - Boarded Up Chest": TWWHDLocationData(
        59, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 1
    ),
    "Dragon Roost Cavern - Swing Across Lava Chest": TWWHDLocationData(
        60, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 13
    ),
    "Dragon Roost Cavern - Rat Room Chest": TWWHDLocationData(
        61, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 14
    ),
    "Dragon Roost Cavern - Rat Room Boarded Up Chest": TWWHDLocationData(
        62, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 3
    ),
    "Dragon Roost Cavern - Bird's Nest": TWWHDLocationData(
        63, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.PCKUP, 3
    ),
    "Dragon Roost Cavern - Dark Room Chest": TWWHDLocationData(
        64, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 4
    ),
    "Dragon Roost Cavern - Pot on Upper Shelf in Pot Room": TWWHDLocationData(
        66, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWHDLocationType.PCKUP, 0
    ),
    "Dragon Roost Cavern - Pot Room Chest": TWWHDLocationData(
        67, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 6
    ),
    "Dragon Roost Cavern - Mini Boss": TWWHDLocationData(
        68, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 17
    ),
    "Dragon Roost Cavern - Under Rope Bridge Chest": TWWHDLocationData(
        69, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 7
    ),
    "Dragon Roost Cavern - Tingle Statue Chest": TWWHDLocationData(
        70, TWWHDFlag.TNGL_CT | TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 15
    ),
    "Dragon Roost Cavern - Big Key Chest": TWWHDLocationData(
        71, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 12
    ),
    "Dragon Roost Cavern - Boss Stairs Right Chest": TWWHDLocationData(
        72, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 11
    ),
    "Dragon Roost Cavern - Boss Stairs Left Chest": TWWHDLocationData(
        73, TWWHDFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWHDLocationType.CHEST, 10
    ),
    "Dragon Roost Cavern - Boss Stairs Right Pot": TWWHDLocationData(
        74, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWHDLocationType.PCKUP, 6
    ),
    "Dragon Roost Cavern - Gohma Heart Container": TWWHDLocationData(
        75, TWWHDFlag.DUNGEON | TWWHDFlag.BOSS, "Gohma Boss Arena", 0x3, TWWHDLocationType.PCKUP, 21
    ),

    # Forest Haven
    "Forest Haven - On Tree Branch": TWWHDLocationData(
        76, TWWHDFlag.ISLND_P, "The Great Sea", 0xB, TWWHDLocationType.PCKUP, 2
    ),
    "Forest Haven - Chest on Small Island": TWWHDLocationData(
        77, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 7
    ),

    # Forbidden Woods
    "Forbidden Woods - First Room Chest": TWWHDLocationData(
        78, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 0
    ),
    "Forbidden Woods - Inside Hollow Tree Chest": TWWHDLocationData(
        79, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 1
    ),
    "Forbidden Woods - Boko Baba Climb Chest": TWWHDLocationData(
        80, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 2
    ),
    "Forbidden Woods - Pot High Above Hollow Tree": TWWHDLocationData(
        81, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Forbidden Woods", 0x4, TWWHDLocationType.PCKUP, 1
    ),
    "Forbidden Woods - Hole In Tree Chest": TWWHDLocationData(
        82, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 6
    ),
    "Forbidden Woods - Morth Pit Chest": TWWHDLocationData(
        83, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 8
    ),
    "Forbidden Woods - Vine Maze Left Chest": TWWHDLocationData(
        84, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 7
    ),
    "Forbidden Woods - Vine Maze Right Chest": TWWHDLocationData(
        85, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 5
    ),
    "Forbidden Woods - Highest Pot in Vine Maze": TWWHDLocationData(
        86, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Forbidden Woods", 0x4, TWWHDLocationType.PCKUP, 22
    ),
    "Forbidden Woods - Tall Room Chest": TWWHDLocationData(
        87, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 12
    ),
    "Forbidden Woods - Mothula Mini Boss Chest": TWWHDLocationData(
        88, TWWHDFlag.DUNGEON, "Forbidden Woods Miniboss Arena", 0x4, TWWHDLocationType.CHEST, 10
    ),
    "Forbidden Woods - Past Seeds Hanging by Vines Chest": TWWHDLocationData(
        89, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 3
    ),
    "Forbidden Woods - Chest Across Hanging Flower": TWWHDLocationData(
        90, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 11
    ),
    "Forbidden Woods - Tingle Statue Chest": TWWHDLocationData(
        91, TWWHDFlag.TNGL_CT | TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 15
    ),
    "Forbidden Woods - Locked Tree Trunk Chest": TWWHDLocationData(
        92, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 9
    ),
    "Forbidden Woods - Big Key Chest": TWWHDLocationData(
        93, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 4
    ),
    "Forbidden Woods - Double Mothula Room Chest": TWWHDLocationData(
        94, TWWHDFlag.DUNGEON, "Forbidden Woods", 0x4, TWWHDLocationType.CHEST, 14
    ),
    "Forbidden Woods - Kalle Demos Heart Container": TWWHDLocationData(
        95, TWWHDFlag.DUNGEON | TWWHDFlag.BOSS, "Kalle Demos Boss Arena", 0x4, TWWHDLocationType.PCKUP, 21
    ),

    # Greatfish Isle
    "Greatfish Isle - Hidden Chest": TWWHDLocationData(
        96, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 6
    ),

    # Tower of the Gods
    "Tower of the Gods - Chest Behind Bombable Wall": TWWHDLocationData(
        97, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 2
    ),
    "Tower of the Gods - Pot Behind Bombable Wall": TWWHDLocationData(
        98, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Tower of the Gods", 0x5, TWWHDLocationType.PCKUP, 0
    ),
    "Tower of the Gods - Hop Across Floating Boxes Chest": TWWHDLocationData(
        99, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 1
    ),
    "Tower of the Gods - Light Two Torches Chest": TWWHDLocationData(
        100, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 10
    ),
    "Tower of the Gods - Skull Room Chest": TWWHDLocationData(
        101, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 3
    ),
    "Tower of the Gods - Shoot Eye Above Skulls Chest": TWWHDLocationData(
        102, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 9
    ),
    "Tower of the Gods - Tingle Statue Chest": TWWHDLocationData(
        103, TWWHDFlag.TNGL_CT | TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 15
    ),
    "Tower of the Gods - First Armos Knights Chest": TWWHDLocationData(
        104, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 6
    ),
    "Tower of the Gods - Stone Tablet": TWWHDLocationData(
        105, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.EVENT, 4, 0x25
    ),
    "Tower of the Gods - Darknut Mini Boss": TWWHDLocationData(
        106, TWWHDFlag.DUNGEON, "Tower of the Gods Miniboss Arena", 0x5, TWWHDLocationType.CHEST, 5
    ),
    "Tower of the Gods - Second Armos Knights Chest": TWWHDLocationData(
        107, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 8
    ),
    "Tower of the Gods - Floating Platforms Room Lower Chest": TWWHDLocationData(
        108, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 4
    ),
    "Tower of the Gods - Floating Platforms Room Upper Chest": TWWHDLocationData(
        109, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 11
    ),
    "Tower of the Gods - Eastern Pot in Big Key Chest Room": TWWHDLocationData(
        110, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Tower of the Gods", 0x5, TWWHDLocationType.PCKUP, 1
    ),
    "Tower of the Gods - Big Key Chest": TWWHDLocationData(
        111, TWWHDFlag.DUNGEON, "Tower of the Gods", 0x5, TWWHDLocationType.CHEST, 0
    ),
    "Tower of the Gods - Gohdan Heart Container": TWWHDLocationData(
        112, TWWHDFlag.DUNGEON | TWWHDFlag.BOSS, "Gohdan Boss Arena", 0x5, TWWHDLocationType.PCKUP, 21
    ),

    # Hyrule
    "Hyrule Castle - Sword Chamber Chest": TWWHDLocationData(
        113, TWWHDFlag.DUNGEON, "Master Sword Chamber", 0x9, TWWHDLocationType.CHEST, 0
    ),

    # Forsaken Fortress
    "Forsaken Fortress - Phantom Ganon": TWWHDLocationData(
        114, TWWHDFlag.DUNGEON, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 16
    ),
    "Forsaken Fortress - Chest Outside Upper Jail Cell": TWWHDLocationData(
        115, TWWHDFlag.DUNGEON, "The Great Sea", 0x2, TWWHDLocationType.CHEST, 0
    ),
    "Forsaken Fortress - Chest Inside Lower Jail Cell": TWWHDLocationData(
        116, TWWHDFlag.DUNGEON, "The Great Sea", 0x2, TWWHDLocationType.CHEST, 3
    ),
    "Forsaken Fortress - Chest Guarded by Bokoblin": TWWHDLocationData(
        117, TWWHDFlag.DUNGEON, "The Great Sea", 0x2, TWWHDLocationType.CHEST, 2
    ),
    "Forsaken Fortress - Chest on Bed": TWWHDLocationData(
        118, TWWHDFlag.DUNGEON, "The Great Sea", 0x2, TWWHDLocationType.CHEST, 1
    ),
    "Forsaken Fortress - Helmaroc King Heart Container": TWWHDLocationData(
        119, TWWHDFlag.DUNGEON | TWWHDFlag.BOSS, "Helmaroc King Boss Arena", 0x2, TWWHDLocationType.PCKUP, 21
    ),

    # Mother and Child Isles
    "Mother & Child Isles - Inside Mother Isle": TWWHDLocationData(
        120, TWWHDFlag.MISCELL, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 28
    ),

    # Fire Mountain
    "Fire Mountain - Interior Chest": TWWHDLocationData(
        121, TWWHDFlag.PZL_CVE | TWWHDFlag.CBT_CVE, "Fire Mountain Secret Cave", 0xC, TWWHDLocationType.CHEST, 0
    ),
    "Fire Mountain - Lookout Platform Chest": TWWHDLocationData(
        122, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 1
    ),
    "Fire Mountain - Lookout Platform Destroy Cannons": TWWHDLocationData(
        123, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 0
    ),
    "Fire Mountain - Big Octo": TWWHDLocationData(
        124, TWWHDFlag.BG_OCTO, "The Great Sea", 0x0, TWWHDLocationType.BOCTO, 0, -60
    ),

    # Ice Ring Isle
    "Ice Ring Isle - Frozen Chest": TWWHDLocationData(
        125, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 18
    ),
    "Ice Ring Isle - Interior Chest": TWWHDLocationData(
        126, TWWHDFlag.PZL_CVE, "Ice Ring Isle Secret Cave", 0xC, TWWHDLocationType.CHEST, 1
    ),
    "Ice Ring Isle - Inner Cave Chest": TWWHDLocationData(
        127, TWWHDFlag.PZL_CVE | TWWHDFlag.CBT_CVE, "Ice Ring Isle Inner Cave", 0xC, TWWHDLocationType.CHEST, 21
    ),

    # Headstone Island
    "Headstone Island - Top of Island": TWWHDLocationData(
        128, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.PCKUP, 8
    ),
    "Headstone Island - Submarine Chest": TWWHDLocationData(
        129, TWWHDFlag.SUBMRIN, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 4
    ),

    # Earth Temple
    "Earth Temple - Warp Pot Room Chest": TWWHDLocationData(
        130, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 0
    ),
    "Earth Temple - Warp Pot Room Behind Curtain": TWWHDLocationData(
        131, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Earth Temple", 0x6, TWWHDLocationType.PCKUP, 0
    ),
    "Earth Temple - First Crypt Chest": TWWHDLocationData(
        132, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 1
    ),
    "Earth Temple - Chest Behind Destructable Wall": TWWHDLocationData(
        133, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 12
    ),
    "Earth Temple - Three Blocks Room Chest": TWWHDLocationData(
        134, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 2
    ),
    "Earth Temple - Behind Statues Chest": TWWHDLocationData(
        135, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 3
    ),
    "Earth Temple - Second Crypt Casket": TWWHDLocationData(
        136, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.PCKUP, 14
    ),
    "Earth Temple - Stalfos Mini Boss": TWWHDLocationData(
        137, TWWHDFlag.DUNGEON, "Earth Temple Miniboss Arena", 0x6, TWWHDLocationType.CHEST, 7
    ),
    "Earth Temple - Tingle Statue Chest": TWWHDLocationData(
        138, TWWHDFlag.TNGL_CT | TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 15
    ),
    "Earth Temple - Foggy Floormaster Room End Chest": TWWHDLocationData(
        139, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 4
    ),
    "Earth Temple - Kill All Floormasters Chest": TWWHDLocationData(
        140, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 11
    ),
    "Earth Temple - Near Hammer Button Behind Curtain": TWWHDLocationData(
        141, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Earth Temple", 0x6, TWWHDLocationType.PCKUP, 1
    ),
    "Earth Temple - Third Crypt Chest": TWWHDLocationData(
        142, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 5
    ),
    "Earth Temple - Many Mirrors Room Right Chest": TWWHDLocationData(
        143, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 9
    ),
    "Earth Temple - Many Mirrors Room Left Chest": TWWHDLocationData(
        144, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 10
    ),
    "Earth Temple - Stalfos Crypt Room Chest": TWWHDLocationData(
        145, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 14
    ),
    "Earth Temple - Big Key Chest": TWWHDLocationData(
        146, TWWHDFlag.DUNGEON, "Earth Temple", 0x6, TWWHDLocationType.CHEST, 6
    ),
    "Earth Temple - Jalhalla Heart Container": TWWHDLocationData(
        147, TWWHDFlag.DUNGEON | TWWHDFlag.BOSS, "Jalhalla Boss Arena", 0x6, TWWHDLocationType.PCKUP, 21
    ),

    # Wind Temple
    "Wind Temple - Between Dirt Patches Chest": TWWHDLocationData(
        148, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 0
    ),
    "Wind Temple - Behind Stone Head in Hidden Upper Room": TWWHDLocationData(
        149, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Wind Temple", 0x7, TWWHDLocationType.PCKUP, 0
    ),
    "Wind Temple - Tingle Statue Chest": TWWHDLocationData(
        150, TWWHDFlag.TNGL_CT | TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 15
    ),
    "Wind Temple - Behind Stone Head Chest": TWWHDLocationData(
        151, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 3
    ),
    "Wind Temple - Left Alcove Chest": TWWHDLocationData(
        152, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 7
    ),
    "Wind Temple - Big Key Chest": TWWHDLocationData(
        153, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 8
    ),
    "Wind Temple - Cyclones Room Chest": TWWHDLocationData(
        154, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 11
    ),
    "Wind Temple - Behind Stone Head in Many Cyclones Room": TWWHDLocationData(
        155, TWWHDFlag.DUNGEON | TWWHDFlag.DG_SCRT, "Wind Temple", 0x7, TWWHDLocationType.PCKUP, 1
    ),
    "Wind Temple - Hub Room Center Chest": TWWHDLocationData(
        156, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 13
    ),
    "Wind Temple - Spike Wall Room First Chest": TWWHDLocationData(
        157, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 9
    ),
    "Wind Temple - Spike Wall Room Destroy Floors": TWWHDLocationData(
        158, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 10
    ),
    "Wind Temple - Wizzrobe Mini Boss": TWWHDLocationData(
        159, TWWHDFlag.DUNGEON, "Wind Temple Miniboss Arena", 0x7, TWWHDLocationType.CHEST, 5
    ),
    "Wind Temple - Hub Room Top Chest": TWWHDLocationData(
        160, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 2
    ),
    "Wind Temple - Behind Armos Chest": TWWHDLocationData(
        161, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 4
    ),
    "Wind Temple - Kill All Basement Room Enemies": TWWHDLocationData(
        162, TWWHDFlag.DUNGEON, "Wind Temple", 0x7, TWWHDLocationType.CHEST, 12
    ),
    "Wind Temple - Molgera Heart Container": TWWHDLocationData(
        163, TWWHDFlag.DUNGEON | TWWHDFlag.BOSS, "Molgera Boss Arena", 0x7, TWWHDLocationType.PCKUP, 21
    ),

    # Ganon's Tower
    "Ganon's Tower - Maze Chest": TWWHDLocationData(
        164, TWWHDFlag.DUNGEON, "The Great Sea", 0x8, TWWHDLocationType.CHEST, 0
    ),

    # Mailbox
    "Mailbox - Letter from Hoskit's Girlfriend": TWWHDLocationData(
        165, TWWHDFlag.MAILBOX | TWWHDFlag.SPOILS, "The Great Sea", 0x0, TWWHDLocationType.SPECL, 0, 0xAE
    ),
    "Mailbox - Letter from Baito's Mother": TWWHDLocationData(
        166, TWWHDFlag.MAILBOX, "The Great Sea", 0x0, TWWHDLocationType.SPECL, 0, 0xAC
    ),
    "Mailbox - Letter from Baito": TWWHDLocationData(
        167, TWWHDFlag.MAILBOX | TWWHDFlag.DUNGEON, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0x7c
    ),
    "Mailbox - Letter from Komali's Father": TWWHDLocationData(
        168, TWWHDFlag.MAILBOX, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0xb5
    ),
    "Mailbox - Letter Advertising Bombs": TWWHDLocationData(
        169, TWWHDFlag.MAILBOX, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0x7D
    ),
    "Mailbox - Letter Advertising Rock Spire Shop Ship": TWWHDLocationData(
        170, TWWHDFlag.MAILBOX, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0x7A
    ),
    # "Mailbox - Beedle's Silver Membership Reward": TWWHDLocationData(
    #     171, TWWHDFlag.OTHER, "The Great Sea"
    # ),
    # "Mailbox - Beedle's Gold Membership Reward": TWWHDLocationData(
    #     172, TWWHDFlag.OTHER, "The Great Sea"
    # ),
    "Mailbox - Letter from Orca": TWWHDLocationData(
        173, TWWHDFlag.MAILBOX | TWWHDFlag.DUNGEON, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0x7b
    ),
    "Mailbox - Letter from Grandma": TWWHDLocationData(
        174, TWWHDFlag.MAILBOX, "The Great Sea", 0x0, TWWHDLocationType.SPECL, 0, 0x9d
    ),
    "Mailbox - Letter from Aryll": TWWHDLocationData(
        175, TWWHDFlag.MAILBOX | TWWHDFlag.DUNGEON, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0x8b
    ),
    "Mailbox - Letter from Tingle": TWWHDLocationData(
        176,
        TWWHDFlag.MAILBOX | TWWHDFlag.DUNGEON | TWWHDFlag.XPENSVE, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0xb2
    ),

    # The Great Sea
    "Great Sea - Beedle Shop 20 Rupee Item": TWWHDLocationData(
        177, TWWHDFlag.MISCELL, "The Great Sea",  0xA, TWWHDLocationType.EVENT, 1, 0x69
    ),
    "Great Sea - Salvage Corp Gift": TWWHDLocationData(
        178, TWWHDFlag.FREE_GF, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 7, 0x69
    ),
    "Great Sea - Cyclos": TWWHDLocationData(
        179, TWWHDFlag.MISCELL, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 4, 0x27
    ),
    "Great Sea - Goron Trading Reward": TWWHDLocationData(
        180, TWWHDFlag.LONG_SQ | TWWHDFlag.XPENSVE, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 2, 0x3E
    ),
    "Great Sea - Withered Trees": TWWHDLocationData(
        181, TWWHDFlag.LONG_SQ, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 5, 0x2E
    ),
    "Great Sea - Ghost Ship Chest": TWWHDLocationData(
        182, TWWHDFlag.MISCELL, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 23
    ),

    # Private Oasis
    "Private Oasis - Top of Waterfall Chest": TWWHDLocationData(
        183, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 19
    ),
    "Private Oasis - Cabana Labyrinth Lower Floor Chest": TWWHDLocationData(
        184, TWWHDFlag.PZL_CVE, "Cabana Labyrinth", 0xC, TWWHDLocationType.CHEST, 22
    ),
    "Private Oasis - Cabana Labyrinth Upper Floor Chest": TWWHDLocationData(
        185, TWWHDFlag.PZL_CVE, "Cabana Labyrinth", 0xC, TWWHDLocationType.CHEST, 17
    ),
    "Private Oasis - Big Octo": TWWHDLocationData(
        186, TWWHDFlag.BG_OCTO, "The Great Sea", 0x0, TWWHDLocationType.BOCTO, 0, -34
    ),

    # Spectacle Island
    "Spectacle Island - Barrel Shooting First Prize": TWWHDLocationData(
        187, TWWHDFlag.MINIGME, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 0, 0xb7
    ),
    "Spectacle Island - Barrel Shooting Second Prize": TWWHDLocationData(
        188, TWWHDFlag.MINIGME, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 1, 0xb7
    ),

    # Needle Rock Isle
    "Needle Rock Isle - Chest": TWWHDLocationData(
        189, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 3
    ),
    "Needle Rock Isle - Cave Chest": TWWHDLocationData(
        190, TWWHDFlag.PZL_CVE, "Needle Rock Isle Secret Cave", 0xD, TWWHDLocationType.CHEST, 9
    ),
    "Needle Rock Isle - Golden Gunboat": TWWHDLocationData(
        191, TWWHDFlag.BG_OCTO, "The Great Sea", 0x0, TWWHDLocationType.BOCTO, 2, -42
    ),

    # Angular Isles
    "Angular Isles - Peak Chest": TWWHDLocationData(
        192, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 0
    ),
    "Angular Isles - Cave Chest": TWWHDLocationData(
        193, TWWHDFlag.PZL_CVE, "Angular Isles Secret Cave", 0xD, TWWHDLocationType.CHEST, 6
    ),

    # Boating Course
    "Boating Course - Raft Chest": TWWHDLocationData(
        194, TWWHDFlag.PLTFRMS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 21
    ),
    "Boating Course - Cave Chest": TWWHDLocationData(
        195, TWWHDFlag.PZL_CVE | TWWHDFlag.CBT_CVE, "Boating Course Secret Cave", 0xD, TWWHDLocationType.CHEST, 15
    ),

    # Stone Watcher Island
    "Stone Watcher Island - Cave Chest": TWWHDLocationData(
        196, TWWHDFlag.CBT_CVE, "Stone Watcher Island Secret Cave", 0xC, TWWHDLocationType.CHEST, 10
    ),
    "Stone Watcher Island - Lookout Platform Chest": TWWHDLocationData(
        197, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 18
    ),
    "Stone Watcher Island - Lookout Platform Destroy Cannons": TWWHDLocationData(
        198, TWWHDFlag.PLTFRMS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 20
    ),

    # Islet of Steel
    "Islet of Steel - Interior Chest": TWWHDLocationData(
        199, TWWHDFlag.MISCELL, "The Great Sea", 0xC, TWWHDLocationType.CHEST, 4
    ),
    "Islet of Steel - Lookout Platform Defeat Enemies": TWWHDLocationData(
        200, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 16
    ),

    # Overlook Island
    "Overlook Island - Cave Chest": TWWHDLocationData(
        201, TWWHDFlag.CBT_CVE, "Overlook Island Secret Cave", 0xC, TWWHDLocationType.CHEST, 11
    ),

    # Bird's Peak Rock
    "Birds Peak Rock - Cave Chest": TWWHDLocationData(
        202, TWWHDFlag.PZL_CVE, "Birds Peak Rock Secret Cave", 0xC, TWWHDLocationType.CHEST, 16
    ),

    # Pawprint Isle
    "Pawprint Isle - Chu Chu Cave Chest": TWWHDLocationData(
        203, TWWHDFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWHDLocationType.CHEST, 26
    ),
    "Pawprint Isle - Chu Chu Cave Chest Behind Left Boulder": TWWHDLocationData(
        204, TWWHDFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWHDLocationType.CHEST, 24
    ),
    "Pawprint Isle - Chu Chu Cave Chest Behind Right Boulder": TWWHDLocationData(
        205, TWWHDFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWHDLocationType.CHEST, 25
    ),
    "Pawprint Isle - Chu Chu Cave Chest Scale Wall": TWWHDLocationData(
        206, TWWHDFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWHDLocationType.CHEST, 2
    ),
    "Pawprint Isle - Wizzrobe Cave Chest": TWWHDLocationData(
        207, TWWHDFlag.CBT_CVE, "Pawprint Isle Wizzrobe Cave", 0xD, TWWHDLocationType.CHEST, 2
    ),
    "Pawprint Isle - Lookout Platform Defeat Enemies": TWWHDLocationData(
        208, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 5
    ),

    # Thorned Fairy Island
    "Thorned Fairy Island - Great Fairy": TWWHDLocationData(
        209, TWWHDFlag.GRT_FRY, "Thorned Fairy Fountain", 0xC, TWWHDLocationType.EVENT, 0, 0x30
    ),
    "Thorned Fairy Island - Northeastern Lookout Platform Destroy Cannons": TWWHDLocationData(
        210, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 14
    ),
    "Thorned Fairy Island - Southwestern Lookout Platform Defeat Enemies": TWWHDLocationData(
        211, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 15
    ),

    # Eastern Fairy Island
    "Eastern Fairy Island - Great Fairy": TWWHDLocationData(
        212, TWWHDFlag.GRT_FRY, "Eastern Fairy Fountain", 0xC, TWWHDLocationType.EVENT, 3, 0x30
    ),
    "Eastern Fairy Island - Lookout Platform Defeat Cannons and Enemies": TWWHDLocationData(
        213, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 10
    ),

    # Western Fairy Island
    "Western Fairy Island - Great Fairy": TWWHDLocationData(
        214, TWWHDFlag.GRT_FRY, "Western Fairy Fountain", 0xC, TWWHDLocationType.EVENT, 1, 0x30
    ),
    "Western Fairy Island - Lookout Platform Chest": TWWHDLocationData(
        215, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 6
    ),

    # Southern Fairy Island
    "Southern Fairy Island - Great Fairy": TWWHDLocationData(
        216, TWWHDFlag.GRT_FRY, "Southern Fairy Fountain", 0xC, TWWHDLocationType.EVENT, 2, 0x30
    ),
    "Southern Fairy Island - Lookout Platform Destroy Northwest Cannons": TWWHDLocationData(
        217, TWWHDFlag.PLTFRMS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 23
    ),
    "Southern Fairy Island - Lookout Platform Destroy Southeast Cannons": TWWHDLocationData(
        218, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 17
    ),

    # Northern Fairy Island
    "Northern Fairy Island - Great Fairy": TWWHDLocationData(
        219, TWWHDFlag.GRT_FRY, "Northern Fairy Fountain", 0xC, TWWHDLocationType.EVENT, 5, 0x30
    ),
    "Northern Fairy Island - Submarine Chest": TWWHDLocationData(
        220, TWWHDFlag.SUBMRIN, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 6
    ),

    # Tingle Island
    "Tingle Island - Ankle All Statues Reward": TWWHDLocationData(
        221, TWWHDFlag.MISCELL, "The Great Sea", 0x0, TWWHDLocationType.SPECL, 0
    ),
    "Tingle Island - Big Octo": TWWHDLocationData(
        222, TWWHDFlag.BG_OCTO, "The Great Sea", 0x0, TWWHDLocationType.BOCTO, 0, -66
    ),

    # Diamond Steppe Island
    "Diamond Steppe Island - Maze First Chest": TWWHDLocationData(
        223, TWWHDFlag.PZL_CVE, "Diamond Steppe Island Warp Maze Cave", 0xC, TWWHDLocationType.CHEST, 23
    ),
    "Diamond Steppe Island - Maze Second Chest": TWWHDLocationData(
        224, TWWHDFlag.PZL_CVE, "Diamond Steppe Island Warp Maze Cave", 0xC, TWWHDLocationType.CHEST, 3
    ),
    "Diamond Steppe Island - Big Octo": TWWHDLocationData(
        225, TWWHDFlag.BG_OCTO, "The Great Sea", 0x0, TWWHDLocationType.BOCTO, 0, -28
    ),

    # Bomb Island
    "Bomb Island - Cave Chest": TWWHDLocationData(
        226, TWWHDFlag.PZL_CVE, "Bomb Island Secret Cave", 0xC, TWWHDLocationType.CHEST, 5
    ),
    "Bomb Island - Lookout Platform Defeat Enemies": TWWHDLocationData(
        227, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 3
    ),
    "Bomb Island - Submarine Chest": TWWHDLocationData(
        228, TWWHDFlag.SUBMRIN, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 2
    ),

    # Rock Spire Isle
    "Rock Spire Isle - Cave Chest": TWWHDLocationData(
        229, TWWHDFlag.CBT_CVE, "Rock Spire Isle Secret Cave", 0xC, TWWHDLocationType.CHEST, 8
    ),
    "Rock Spire Isle - Beedle 500 Rupee Item": TWWHDLocationData(
        230, TWWHDFlag.XPENSVE, "The Great Sea", 0xA, TWWHDLocationType.EVENT, 5, 0x20
    ),
    "Rock Spire Isle - Beedle 950 Rupee Item": TWWHDLocationData(
        231, TWWHDFlag.XPENSVE, "The Great Sea", 0xA, TWWHDLocationType.EVENT, 4, 0x20
    ),
    "Rock Spire Isle - Beedle 900 Rupee Item": TWWHDLocationData(
        232, TWWHDFlag.XPENSVE, "The Great Sea", 0xA, TWWHDLocationType.EVENT, 3, 0x20
    ),
    "Rock Spire Isle - Western Lookout Platform Destroy Cannons": TWWHDLocationData(
        233, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 23
    ),
    "Rock Spire Isle - Eastern Lookout Platform Destroy Cannons": TWWHDLocationData(
        234, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 24
    ),
    "Rock Spire Isle - Center Lookout Platform Chest": TWWHDLocationData(
        235, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 25
    ),
    "Rock Spire Isle - Defeat Southeast Gunboat": TWWHDLocationData(
        236, TWWHDFlag.BG_OCTO, "The Great Sea", 0x0, TWWHDLocationType.BOCTO, 0, -68
    ),

    # Shark Island
    "Shark Island - Cave Chest": TWWHDLocationData(
        237, TWWHDFlag.CBT_CVE, "Shark Island Secret Cave", 0xD, TWWHDLocationType.CHEST, 22
    ),

    # Cliff Plateau Isles
    "Cliff Plateau Isles - Cave Chest": TWWHDLocationData(
        238, TWWHDFlag.PZL_CVE, "Cliff Plateau Isles Secret Cave", 0xC, TWWHDLocationType.CHEST, 7
    ),
    "Cliff Plateau Isles - Highest Isle Chest": TWWHDLocationData(
        239, TWWHDFlag.PZL_CVE, "Cliff Plateau Isles Inner Cave", 0x0, TWWHDLocationType.CHEST, 1
    ),
    "Cliff Plateau Isles - Lookout Platform Chest": TWWHDLocationData(
        240, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 19
    ),

    # Crescent Moon Island
    "Crescent Moon Island - Chest on Island": TWWHDLocationData(
        241, TWWHDFlag.MISCELL, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 4
    ),
    "Crescent Moon Island - Submarine Chest": TWWHDLocationData(
        242, TWWHDFlag.SUBMRIN, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 7
    ),

    # Horseshoe Island
    "Horseshoe Island - Play Golf": TWWHDLocationData(
        243, TWWHDFlag.ISLND_P, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 5
    ),
    "Horseshoe Island - Cave Chest": TWWHDLocationData(
        244, TWWHDFlag.CBT_CVE, "Horseshoe Island Secret Cave", 0xD, TWWHDLocationType.CHEST, 1
    ),
    "Horseshoe Island - Northwestern Lookout Platform Chest": TWWHDLocationData(
        245, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 26
    ),
    "Horseshoe Island - Southeastern Lookout Platform Chest": TWWHDLocationData(
        246, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 27
    ),

    # Flight Control Platform
    "Flight Control Platform - First Prize": TWWHDLocationData(
        247, TWWHDFlag.MINIGME, "The Great Sea", 0x0, TWWHDLocationType.EVENT, 6, 0x2b
    ),
    "Flight Control Platform - Submarine Chest": TWWHDLocationData(
        248, TWWHDFlag.SUBMRIN, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 3
    ),

    # Star Island
    "Star Island - Cave Chest": TWWHDLocationData(
        249, TWWHDFlag.CBT_CVE, "Star Island Secret Cave", 0xC, TWWHDLocationType.CHEST, 6
    ),
    "Star Island - Lookout Platform Chest": TWWHDLocationData(
        250, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 4
    ),

    # Star Belt Archipelago
    "Star Belt Archipelago - Lookout Platform Chest": TWWHDLocationData(
        251, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 11
    ),

    # Five Star Isles
    "Five Star Isles - Lookout Platform Destroy Cannons": TWWHDLocationData(
        252, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 2
    ),
    "Five Star Isles - Raft Chest": TWWHDLocationData(
        253, TWWHDFlag.PLTFRMS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 2
    ),
    "Five Star Isles - Submarine Chest": TWWHDLocationData(
        254, TWWHDFlag.SUBMRIN, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 1
    ),

    # Seven Star Isles
    "Seven Star Isles - Center Lookout Platform Chest": TWWHDLocationData(
        255, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 8
    ),
    "Seven Star Isles - Northern Lookout Platform Chest": TWWHDLocationData(
        256, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 7
    ),
    "Seven Star Isles - Southern Lookout Platform Chest": TWWHDLocationData(
        257, TWWHDFlag.PLTFRMS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 22
    ),
    "Seven Star Isles - Big Octo": TWWHDLocationData(
        258, TWWHDFlag.BG_OCTO, "The Great Sea", 0x0, TWWHDLocationType.BOCTO, 0, -88
    ),

    # Cyclops Reef
    "Cyclops Reef - Destroy Cannons and Gunboats": TWWHDLocationData(
        259, TWWHDFlag.EYE_RFS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 11
    ),
    "Cyclops Reef - Lookout Platform Defeat Enemies": TWWHDLocationData(
        260, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 12
    ),

    # Two Eye Reef
    "Two Eye Reef - Destroy Cannons and Gunboats": TWWHDLocationData(
        261, TWWHDFlag.EYE_RFS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 13
    ),
    "Two Eye Reef - Lookout Platform Chest": TWWHDLocationData(
        262, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 21
    ),
    "Two Eye Reef - Big Octo Great Fairy": TWWHDLocationData(
        263, TWWHDFlag.BG_OCTO | TWWHDFlag.GRT_FRY, "The Great Sea", 0x0, TWWHDLocationType.SWTCH, 52
    ),

    # Three Eye Reef
    "Three Eye Reef - Destroy Cannons and Gunboats": TWWHDLocationData(
        264, TWWHDFlag.EYE_RFS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 12
    ),

    # Four Eye Reef
    "Four Eye Reef - Destroy Cannons and Gunboats": TWWHDLocationData(
        265, TWWHDFlag.EYE_RFS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 14
    ),

    # Five Eye Reef
    "Five Eye Reef - Destroy Cannons": TWWHDLocationData(
        266, TWWHDFlag.EYE_RFS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 15
    ),
    "Five Eye Reef - Lookout Platform Chest": TWWHDLocationData(
        267, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 20
    ),

    # Six Eye Reef
    "Six Eye Reef - Destroy Cannons and Gunboats": TWWHDLocationData(
        268, TWWHDFlag.EYE_RFS, "The Great Sea", 0x0, TWWHDLocationType.CHEST, 17
    ),
    "Six Eye Reef - Lookout Platform Destroy Cannons": TWWHDLocationData(
        269, TWWHDFlag.PLTFRMS, "The Great Sea", 0x1, TWWHDLocationType.CHEST, 13
    ),
    "Six Eye Reef - Submarine Chest": TWWHDLocationData(
        270, TWWHDFlag.SUBMRIN, "The Great Sea", 0xA, TWWHDLocationType.CHEST, 0
    ),

    # Sunken Treasure
    "Forsaken Fortress Sector - Sunken Treasure": TWWHDLocationData(
        271, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 8
    ),
    "Star Island - Sunken Treasure": TWWHDLocationData(
        272, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 18
    ),
    "Northern Fairy Island - Sunken Treasure": TWWHDLocationData(
        273, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 51
    ),
    "Gale Isle - Sunken Treasure": TWWHDLocationData(
        274, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 33
    ),
    "Crescent Moon Island - Sunken Treasure": TWWHDLocationData(
        275, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 40
    ),
    "Seven Star Isles - Sunken Treasure": TWWHDLocationData(
        276, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 38
    ),
    "Overlook Island - Sunken Treasure": TWWHDLocationData(
        277, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 15
    ),
    "Four Eye Reef - Sunken Treasure": TWWHDLocationData(
        278, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 12
    ),
    "Mother & Child Isles - Sunken Treasure": TWWHDLocationData(
        279, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 56
    ),
    "Spectacle Island - Sunken Treasure": TWWHDLocationData(
        280, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 5
    ),
    "Windfall Island - Sunken Treasure": TWWHDLocationData(
        281, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 58
    ),
    "Pawprint Isle - Sunken Treasure": TWWHDLocationData(
        282, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 42
    ),
    "Dragon Roost Island - Sunken Treasure": TWWHDLocationData(
        283, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 50
    ),
    "Flight Control Platform - Sunken Treasure": TWWHDLocationData(
        284, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 13
    ),
    "Western Fairy Island - Sunken Treasure": TWWHDLocationData(
        285, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 10
    ),
    "Rock Spire Isle - Sunken Treasure": TWWHDLocationData(
        286, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 48
    ),
    "Tingle Island - Sunken Treasure": TWWHDLocationData(
        287, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 0
    ),
    "Northern Triangle Island - Sunken Treasure": TWWHDLocationData(
        288, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 11
    ),
    "Eastern Fairy Island - Sunken Treasure": TWWHDLocationData(
        289, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 62
    ),
    "Fire Mountain - Sunken Treasure": TWWHDLocationData(
        290, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 9
    ),
    "Star Belt Archipelago - Sunken Treasure": TWWHDLocationData(
        291, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 17
    ),
    "Three Eye Reef - Sunken Treasure": TWWHDLocationData(
        292, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 49
    ),
    "Greatfish Isle - Sunken Treasure": TWWHDLocationData(
        293, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 32
    ),
    "Cyclops Reef - Sunken Treasure": TWWHDLocationData(
        294, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 16
    ),
    "Six Eye Reef - Sunken Treasure": TWWHDLocationData(
        295, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 52
    ),
    "Tower of the Gods Sector - Sunken Treasure": TWWHDLocationData(
        296, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 1
    ),
    "Eastern Triangle Island - Sunken Treasure": TWWHDLocationData(
        297, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 57
    ),
    "Thorned Fairy Island - Sunken Treasure": TWWHDLocationData(
        298, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 44
    ),
    "Needle Rock Isle - Sunken Treasure": TWWHDLocationData(
        299, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 60
    ),
    "Islet of Steel - Sunken Treasure": TWWHDLocationData(
        300, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 54
    ),
    "Stone Watcher Island - Sunken Treasure": TWWHDLocationData(
        301, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 34
    ),
    "Southern Triangle Island - Sunken Treasure": TWWHDLocationData(
        302, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 37
    ),
    "Private Oasis - Sunken Treasure": TWWHDLocationData(
        303, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 55
    ),
    "Bomb Island - Sunken Treasure": TWWHDLocationData(
        304, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 43
    ),
    "Birds Peak Rock - Sunken Treasure": TWWHDLocationData(
        305, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 6
    ),
    "Diamond Steppe Island - Sunken Treasure": TWWHDLocationData(
        306, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 45
    ),
    "Five Eye Reef - Sunken Treasure": TWWHDLocationData(
        307, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 53
    ),
    "Shark Island - Sunken Treasure": TWWHDLocationData(
        308, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 59
    ),
    "Southern Fairy Island - Sunken Treasure": TWWHDLocationData(
        309, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 61
    ),
    "Ice Ring Isle - Sunken Treasure": TWWHDLocationData(
        310, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 7
    ),
    "Forest Haven - Sunken Treasure": TWWHDLocationData(
        311, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 46
    ),
    "Cliff Plateau Isles - Sunken Treasure": TWWHDLocationData(
        312, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 36
    ),
    "Horseshoe Island - Sunken Treasure": TWWHDLocationData(
        313, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 4
    ),
    "Outset Island - Sunken Treasure": TWWHDLocationData(
        314, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 35
    ),
    "Headstone Island - Sunken Treasure": TWWHDLocationData(
        315, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 63
    ),
    "Two Eye Reef - Sunken Treasure": TWWHDLocationData(
        316, TWWHDFlag.TRI_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 39
    ),
    "Angular Isles - Sunken Treasure": TWWHDLocationData(
        317, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 41
    ),
    "Boating Course - Sunken Treasure": TWWHDLocationData(
        318, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 14
    ),
    "Five Star Isles - Sunken Treasure": TWWHDLocationData(
        319, TWWHDFlag.TRE_CHT, "The Great Sea", 0x0, TWWHDLocationType.CHART, 47
    ),

    # Defeat Ganondorf
    "Defeat Ganondorf": TWWHDLocationData(
        None, TWWHDFlag.ALWAYS, "The Great Sea", 0x8, TWWHDLocationType.SWTCH, 64
    ),
}


ISLAND_NAME_TO_SALVAGE_BIT: dict[str, int] = {
    "Forsaken Fortress Sector": 8,
    "Star Island": 18,
    "Northern Fairy Island": 51,
    "Gale Isle": 33,
    "Crescent Moon Island": 40,
    "Seven Star Isles": 38,
    "Overlook Island": 15,
    "Four Eye Reef": 12,
    "Mother & Child Isles": 56,
    "Spectacle Island": 5,
    "Windfall Island": 58,
    "Pawprint Isle": 42,
    "Dragon Roost Island": 50,
    "Flight Control Platform": 13,
    "Western Fairy Island": 10,
    "Rock Spire Isle": 48,
    "Tingle Island": 0,
    "Northern Triangle Island": 11,
    "Eastern Fairy Island": 62,
    "Fire Mountain": 9,
    "Star Belt Archipelago": 17,
    "Three Eye Reef": 49,
    "Greatfish Isle": 32,
    "Cyclops Reef": 16,
    "Six Eye Reef": 52,
    "Tower of the Gods Sector": 1,
    "Eastern Triangle Island": 57,
    "Thorned Fairy Island": 44,
    "Needle Rock Isle": 60,
    "Islet of Steel": 54,
    "Stone Watcher Island": 34,
    "Southern Triangle Island": 37,
    "Private Oasis": 55,
    "Bomb Island": 43,
    "Birds Peak Rock": 6,
    "Diamond Steppe Island": 45,
    "Five Eye Reef": 53,
    "Shark Island": 59,
    "Southern Fairy Island": 61,
    "Ice Ring Isle": 7,
    "Forest Haven": 46,
    "Cliff Plateau Isles": 36,
    "Horseshoe Island": 4,
    "Outset Island": 35,
    "Headstone Island": 63,
    "Two Eye Reef": 39,
    "Angular Isles": 41,
    "Boating Course": 14,
    "Five Star Isles": 47,
}


def split_location_name_by_zone(location_name: str) -> tuple[str, str]:
    """
    Split a location name into its zone name and specific name.

    :param location_name: The full name of the location.
    :return: A tuple containing the zone and specific name.
    """
    if " - " in location_name:
        zone_name, specific_location_name = location_name.split(" - ", 1)
    else:
        zone_name = specific_location_name = location_name

    return zone_name, specific_location_name

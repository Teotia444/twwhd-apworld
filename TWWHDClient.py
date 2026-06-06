import asyncio
import time
import traceback
from typing import TYPE_CHECKING, Any, Optional

import pymem

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus

from .Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from .Locations import ISLAND_NAME_TO_SALVAGE_BIT, LOCATION_TABLE, TWWHDLocation, TWWHDLocationData, TWWHDLocationType
from .randomizers.Charts import ISLAND_NUMBER_TO_NAME

if TYPE_CHECKING:
    import kvui

CONNECTION_REFUSED_GAME_STATUS = (
    "Cemu failed to connect. Please load a randomized ROM for The Wind Waker HD. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Cemu failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Cemu connection was lost. Please restart your emulator and make sure The Wind Waker HD is running."
)
CONNECTION_CONNECTED_STATUS = "Cemu connected successfully."
CONNECTION_INITIAL_STATUS = "Cemu connection has not been initiated."


# This address is used to check/set the player's health for DeathLink.
CURR_HEALTH_ADDR = 0x145b7b82

# These addresses are used for the Moblin's Letter check.
LETTER_BASE_ADDR = 0x803C4C8E
LETTER_OWND_ADDR = 0x803C4C98

# These addresses are used to check flags for locations.
CHARTS_BITFLD_ADDR = 0x145B7C70
BASE_CHESTS_BITFLD_ADDR = 0x145B7F00
BASE_SWITCHES_BITFLD_ADDR = 0x145B7F04
BASE_PICKUPS_BITFLD_ADDR = 0x145B7F14
CURR_STAGE_CHESTS_BITFLD_ADDR = 0x145B82F8
CURR_STAGE_SWITCHES_BITFLD_ADDR = 0x145B82FC
CURR_STAGE_PICKUPS_BITFLD_ADDR = 0x145B830C

# The expected index for the following item that should be received. Uses event bits 0x60 and 0x61.
EXPECTED_INDEX_ADDR = 0x145B81F8

# These bytes contain whether the player has been rewarded for finding a particular Tingle statue.
TINGLE_STATUE_1_ADDR = 0x803C523E  # 0x40 is the bit for the Dragon Tingle statue.
TINGLE_STATUE_2_ADDR = 0x803C5249  # 0x0F are the bits for the remaining Tingle statues.

# This address contains the current stage ID.
CURR_STAGE_ID_ADDR = 0x145b831c

# This address is used to check the stage name to verify that the player is in-game before sending items.
CURR_STAGE_NAME_ADDR = 0x104741F0

# This address is the start of an array that we use to inform us of which charts lead where.
# The array is of length 49, and each element is two bytes. The index represents the chart's original destination, and
# the value represents the new destination.
# The chart name is inferrable from the chart's original destination.
CHARTS_MAPPING_ADDR = 0x803FE8E0

# Data storage key
AP_VISITED_STAGE_NAMES_KEY_FORMAT = "twwhd_visited_stages_%i"

TWWHDMemory : pymem.Pymem = None



class TWWHDCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for The Wind Waker HD client commands.

    This class handles commands specific to The Wind Waker HD.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_cemu(self) -> None:
        """
        Display the current Cemu emulator connection status.
        """
        if isinstance(self.ctx, TWWHDContext):
            logger.info(f"Cemu Status: {self.ctx.cemu_status}")

    def _cmd_attach(self, base_addr: str) -> None:
        """
        Connects to Cemu.

        :param base_addr: The base cemu address.
        """
        if isinstance(self.ctx, TWWHDContext) and self.ctx.auth:
            self.ctx.CEMU_BASE_ADDR = int(base_addr, base=16)
            self.ctx.cemu_sync_task = asyncio.create_task(cemu_sync_task(self.ctx), name="CemuSync")
        elif isinstance(self.ctx, TWWHDContext) and not self.ctx.auth:
            logger.info(f"Connect to the AP room before connecting Cemu!")
            


class TWWHDContext(CommonContext):
    """
    The context for The Wind Waker HD client.

    This class manages all interactions with the Cemu emulator and the Archipelago server for The Wind Waker HD.
    """

    command_processor = TWWHDCommandProcessor
    game: str = "The Wind Waker HD"
    items_handling: int = 0b111

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the TWWHD context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """

        super().__init__(server_address, password)
        self.cemu_sync_task: Optional[asyncio.Task[None]] = None
        self.cemu_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.has_send_death: bool = False

        # Bitfields used for checking locations.
        self.charts_bitfield: int
        self.chests_bitfields: dict[int, int]
        self.switches_bitfields: dict[int, int]
        self.pickups_bitfields: dict[int, int]
        self.curr_stage_chests_bitfield: int
        self.curr_stage_switches_bitfield: int
        self.curr_stage_pickups_bitfield: int

        # Keep track of when the player received their first progressive magic meter.
        self.received_magic_idx: int = -1

        # A dictionary that maps salvage locations to their sunken treasure bit.
        self.salvage_locations_map: dict[str, int] = {}

        # Name of the current stage as read from the game's memory. Sent to trackers whenever its value changes to
        # facilitate automatically switching to the map of the current stage.
        self.current_stage_name: str = ""

        # Set of visited stages. A dictionary (used as a set) of all visited stages is set in the server's data storage
        # and updated when the player visits a new stage for the first time. To track which stages are new and need to
        # cause the server's data storage to update, the TWW AP Client keeps track of the visited stages in a set.
        # Trackers can request the dictionary from data storage to see which stages the player has visited.
        # It starts as `None` until it has been read from the server.
        self.visited_stage_names: Optional[set[str]] = None

        self.CEMU_BASE_ADDR: int = 0x0

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect the client from the server and reset game state variables.

        :param allow_autoreconnect: Allow the client to auto-reconnect to the server. Defaults to `False`.

        """
        self.auth = None
        self.salvage_locations_map = {}
        self.current_stage_name = ""
        self.visited_stage_names = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            await self.get_username()
            await self.send_connect()
            

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        if cmd == "Connected":
            self.update_salvage_locations_map()
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
            # Request the connected slot's dictionary (used as a set) of visited stages.
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            Utils.async_start(self.send_msgs([{"cmd": "Get", "keys": [visited_stages_key]}]))
        elif cmd == "Retrieved":
            requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            if self.slot is not None:
                visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
                if visited_stages_key in requested_keys_dict:
                    visited_stages = requested_keys_dict[visited_stages_key]
                    # If it has not been set before, the value in the response will be `None`.
                    visited_stage_names = set() if visited_stages is None else set(visited_stages.keys())
                    # If the current stage name is not in the set, send a message to update the dictionary on the
                    # server.
                    current_stage_name = self.current_stage_name
                    if current_stage_name and current_stage_name not in visited_stage_names:
                        visited_stage_names.add(current_stage_name)
                        Utils.async_start(self.update_visited_stages(current_stage_name))
                    self.visited_stage_names = visited_stage_names

    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        _give_death(self)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for The Wind Waker HD client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = "Archipelago The Wind Waker HD Client"
        return ui

    async def update_visited_stages(self, newly_visited_stage_name: str) -> None:
        """
        Update the server's data storage of the visited stage names to include the newly visited stage name.

        :param newly_visited_stage_name: The name of the stage recently visited.
        """
        if self.slot is not None:
            visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
            await self.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": visited_stages_key,
                        "default": {},
                        "want_reply": False,
                        "operations": [{"operation": "update", "value": {newly_visited_stage_name: True}}],
                    }
                ]
            )

    def update_salvage_locations_map(self) -> None:
        """
        Update the client's mapping of salvage locations to their bitfield bit.

        This is necessary for the client to handle randomized charts correctly.
        """
        self.salvage_locations_map = {}
        for offset in range(49):
            island_name = ISLAND_NUMBER_TO_NAME[offset + 1]
            salvage_bit = ISLAND_NAME_TO_SALVAGE_BIT[island_name]
            shuffled_island_number = offset + 1 # TODO: chart randomizer
            shuffled_island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
            salvage_location_name = f"{shuffled_island_name} - Sunken Treasure"
            self.salvage_locations_map[salvage_location_name] = salvage_bit


def read_short(ctx: TWWHDContext, console_address: int) -> int:
    """
    Read a 2-byte short from Cemu memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    global TWWHDMemory
    return TWWHDMemory.read_short(ctx.CEMU_BASE_ADDR + console_address)


def write_short(ctx:TWWHDContext, console_address: int, value: int) -> None:
    """
    Write a 2-byte short to Cemu memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    global TWWHDMemory
    TWWHDMemory.write_short(ctx.CEMU_BASE_ADDR+console_address, value)


def read_string(ctx:TWWHDContext, console_address: int, strlen: int) -> str:
    """
    Read a string from Cemu memory.

    :param console_address: Address to start reading from.
    :param strlen: Length of the string to read.
    :return: The string.
    """
    global TWWHDMemory
    return TWWHDMemory.read_string(ctx.CEMU_BASE_ADDR+console_address, strlen)


def _give_death(ctx: TWWHDContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: The Wind Waker HD client context.
    """
    global TWWHDMemory
    if (
        ctx.slot is not None
        and TWWHDMemory is not None
        and ctx.cemu_status == CONNECTION_CONNECTED_STATUS
        and check_ingame(ctx)
    ):
        ctx.has_send_death = True
        write_short(ctx, CURR_HEALTH_ADDR, 0)

def default_give_item(ctx:TWWHDContext, id:int):
    global TWWHDMemory
    b = TWWHDMemory.write_uchar(ctx.CEMU_BASE_ADDR + 0x28F8844, id) 
    return b

    

def _give_item(ctx: TWWHDContext, item_name: str) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The Wind Waker client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    if not check_ingame(ctx) or not (TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR + 0x28F8844) == 0xFF):
        return False
    
    default_give_item(ctx, ITEM_TABLE[item_name].item_id)
    return True


async def give_items(ctx: TWWHDContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: The Wind Waker HD client context.
    """
    if check_ingame(ctx):

        # Clear all the fathers letters that the player might have collected, they're fake items
        for i in range(10):
            if(TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR + 0x145B7C06 + i) == 0x98): #fathers letter id
                TWWHDMemory.write_uchar(ctx.CEMU_BASE_ADDR + 0x145B7C06 + i, 0xFF)

        # Read the expected index of the player, which is the index of the next item they're expecting to receive.
        # The expected index starts at 0 for a fresh save file.
        expected_idx = read_short(ctx, EXPECTED_INDEX_ADDR)

        # Check if there are new items.
        received_items = ctx.items_received
        if len(received_items) <= expected_idx:
            # There are no new items.
            return

        # Loop through items to give.
        # Give the player all items at an index greater than or equal to the expected index.
        for idx, item in enumerate(received_items[expected_idx:], start=expected_idx):
            # Attempt to give the item and increment the expected index.
            while not _give_item(ctx, LOOKUP_ID_TO_NAME[item.item]):
                await asyncio.sleep(0.01)
                if not check_ingame(ctx):
                    return

            # Increment the expected index.
            write_short(ctx, EXPECTED_INDEX_ADDR, idx + 1)


def check_special_location(ctx:TWWHDContext, location_name: str, data: TWWHDLocationData) -> bool:
    """
    Check that the player has checked a given location.
    This function handles locations that require special logic.

    :param location_name: The name of the location.
    :param data: The data associated with the location.
    :raises NotImplementedError: If an unknown location name is provided.
    """
    checked = False

    # For "Windfall Island - Lenzo's House - Become Lenzo's Assistant"
    # 0x6 is delivered the final picture for Lenzo, 0x7 is a day has passed since becoming his assistant
    # Either is fine for sending the check, so check both conditions. TODO
    # if location_name == "Windfall Island - Lenzo's House - Become Lenzo's Assistant":
    #     checked = (
    #         TWWHDMemory.read_bool(0x145B81A4 + data.address) & 0x6 == 0x6
    #         or TWWHDMemory.read_bool(0x145B81A4 + data.address) & 0x7 == 0x7
    #     )

    # The "Windfall Island - Maggie - Delivery Reward" flag remains unknown.
    # However, as a temporary workaround, we can check if the player had Moblin's letter at some point, but it's no
    # longer in their Delivery Bag.
    # elif location_name == "Windfall Island - Maggie - Delivery Reward":
    #     was_moblins_owned = (TWWHDMemory.read_long(LETTER_OWND_ADDR) >> 15) & 1
    #     dbag_contents = [TWWHDMemory.read_bool(LETTER_BASE_ADDR + offset) for offset in range(8)]
    #     checked = was_moblins_owned and 0x9B not in dbag_contents

    # For Letter from Hoskit's Girlfriend, we need to check two bytes.
    # 0x1 = Golden Feathers delivered, 0x2 = Mail sent by Hoskit's Girlfriend, 0x3 = Mail read by Link
    global TWWHDMemory
    if location_name == "Mailbox - Letter from Hoskit's Girlfriend":
        checked = TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR + 0x145B81A4 + data.address) & 0x3 == 0x3

    # For Letter from Baito's Mother, we need to check two bytes.
    # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
    if location_name == "Mailbox - Letter from Baito's Mother":
        checked = TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR + 0x145B81A4 + data.address) & 0x3 == 0x3

    # For Letter from Grandma, we need to check two bytes.
    # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
    if location_name == "Mailbox - Letter from Grandma":
        checked = TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR + 0x145B81A4 + data.address) & 0x3 == 0x3

    # We check if the bits for turning all five statues are set for the Ankle's reward.
    # For some reason, the bit for the Dragon Tingle Statue is separate from the rest.
    #elif location_name == "Tingle Island - Ankle - Reward for All Tingle Statues":
    #    dragon_tingle_statue_rewarded = TWWHDMemory.read_bool(TINGLE_STATUE_1_ADDR) & 0x40 == 0x40
    #    other_tingle_statues_rewarded = TWWHDMemory.read_bool(TINGLE_STATUE_2_ADDR) & 0x0F == 0x0F
    #    checked = dragon_tingle_statue_rewarded and other_tingle_statues_rewarded

    # else:
    #     raise NotImplementedError(f"Unknown special location: {location_name}")

    return checked


def check_regular_location(ctx: TWWHDContext, curr_stage_id: int, data: TWWHDLocationData) -> bool:
    """
    Check that the player has checked a given location.
    This function handles locations that only require checking that a particular bit is set.

    The check looks at the saved data for the stage at which the location is located and the data for the current stage.
    In the latter case, this data includes data that has not yet been written to the saved data.

    :param ctx: The Wind Waker client context.
    :param curr_stage_id: The current stage at which the player is.
    :param data: The data associated with the location.
    :raises NotImplementedError: If a location with an unknown type is provided.
    """
    checked = False

    # Check the saved bitfields for the stage.
    if data.type == TWWHDLocationType.CHEST:
        checked = bool((ctx.chests_bitfields[data.stage_id] >> data.bit) & 1)
    elif data.type == TWWHDLocationType.SWTCH:
        checked = bool((ctx.switches_bitfields[data.stage_id] >> data.bit) & 1)
    elif data.type == TWWHDLocationType.PCKUP:
        checked = bool((ctx.pickups_bitfields[data.stage_id] >> data.bit) & 1)
    else:
        raise NotImplementedError(f"Unknown location type: {data.type}")

    # If the location is in the current stage, check the bitfields for the current stage as well.
    if not checked and curr_stage_id == data.stage_id:
        if data.type == TWWHDLocationType.CHEST:
            checked = bool((ctx.curr_stage_chests_bitfield >> data.bit) & 1)
        elif data.type == TWWHDLocationType.SWTCH:
            checked = bool((ctx.curr_stage_switches_bitfield >> data.bit) & 1)
        elif data.type == TWWHDLocationType.PCKUP:
            checked = bool((ctx.curr_stage_pickups_bitfield >> data.bit) & 1)
        else:
            raise NotImplementedError(f"Unknown location type: {data.type}")

    return checked


async def check_locations(ctx: TWWHDContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: The Wind Waker client context.
    """
    global TWWHDMemory
    # Read the bitfield for sunken treasure locations.
    ctx.charts_bitfield = int.from_bytes(TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR + CHARTS_BITFLD_ADDR, 8), byteorder="big")

    # Read the bitfields once before the loop to speed things up a bit.
    ctx.chests_bitfields = {}
    ctx.switches_bitfields = {}
    ctx.pickups_bitfields = {}
    for stage_id in range(0xE):
        chest_bitfield_addr = BASE_CHESTS_BITFLD_ADDR + (0x24 * stage_id)
        switches_bitfield_addr = BASE_SWITCHES_BITFLD_ADDR + (0x24 * stage_id)
        pickups_bitfield_addr = BASE_PICKUPS_BITFLD_ADDR + (0x24 * stage_id)

        ctx.chests_bitfields[stage_id] = int.from_bytes(
            TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR + chest_bitfield_addr, 0x4), byteorder="big"
        )
        ctx.switches_bitfields[stage_id] = int.from_bytes(
            TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR + switches_bitfield_addr, 10), byteorder="big"
        )
        ctx.pickups_bitfields[stage_id] = int.from_bytes(
            TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR + pickups_bitfield_addr, 0x4), byteorder="big"
        )

    ctx.curr_stage_chests_bitfield = int.from_bytes(
        TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR + CURR_STAGE_CHESTS_BITFLD_ADDR, 0x4), byteorder="big"
    )
    ctx.curr_stage_switches_bitfield = int.from_bytes(
        TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR + CURR_STAGE_SWITCHES_BITFLD_ADDR, 10), byteorder="big"
    )
    ctx.curr_stage_pickups_bitfield = int.from_bytes(
        TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR + CURR_STAGE_PICKUPS_BITFLD_ADDR, 0x4), byteorder="big"
    )

    # We check which locations are currently checked on the current stage.
    curr_stage_id = TWWHDMemory.read_short(ctx.CEMU_BASE_ADDR + CURR_STAGE_ID_ADDR)

    # Loop through all locations to see if each has been checked.
    for location, data in LOCATION_TABLE.items():
        checked = False
        if data.type == TWWHDLocationType.CHART:
            if location in ctx.salvage_locations_map: 
                salvage_bit = ctx.salvage_locations_map[location]
                checked = bool((ctx.charts_bitfield >> salvage_bit) & 1)
        elif data.type == TWWHDLocationType.BOCTO:
            assert data.address is not None
            checked = bool((TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR + 0x145B81A5 + data.address) >> data.bit) & 1)
        elif data.type == TWWHDLocationType.EVENT:
            checked = bool((TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR + 0x145B81A4 + data.address) >> data.bit) & 1)
        elif data.type == TWWHDLocationType.SPECL:
            checked = check_special_location(ctx, location, data)
        else:
            checked = check_regular_location(ctx, curr_stage_id, data)

        if checked:
            if data.code is None:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
            else:
                ctx.locations_checked.add(TWWHDLocation.get_apid(data.code))

    # Send the list of newly-checked locations to the server.
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])


async def check_current_stage_changed(ctx: TWWHDContext) -> None:
    """
    Check if the player has moved to a new stage.
    If so, update all trackers with the new stage name.
    If the stage has never been visited, additionally update the server.

    :param ctx: The Wind Waker client context.
    """
    new_stage_name = read_string(ctx, CURR_STAGE_NAME_ADDR, 8)

    current_stage_name = ctx.current_stage_name
    if new_stage_name != current_stage_name:
        ctx.current_stage_name = new_stage_name
        # Send a Bounced message containing the new stage name to all trackers connected to the current slot.
        data_to_send = {"twwhd_stage_name": new_stage_name}
        message = {
            "cmd": "Bounce",
            "slots": [ctx.slot],
            "data": data_to_send,
        }
        await ctx.send_msgs([message])

        # If the stage has never been visited before, update the server's data storage to indicate that it has been
        # visited.
        visited_stage_names = ctx.visited_stage_names
        if visited_stage_names is not None and new_stage_name not in visited_stage_names:
            visited_stage_names.add(new_stage_name)
            await ctx.update_visited_stages(new_stage_name)


async def check_alive(ctx:TWWHDContext) -> bool:
    """
    Check if the player is currently alive in-game.

    :return: `True` if the player is alive, otherwise `False`.
    """
    cur_health = read_short(ctx, CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TWWHDContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.slot is not None and check_ingame(ctx):
        cur_health = read_short(ctx, CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False


def check_ingame(ctx: TWWHDContext) -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    return read_string(ctx, CURR_STAGE_NAME_ADDR, 8) not in ["", "sea_T", "Name"]


async def cemu_sync_task(ctx: TWWHDContext) -> None:
    """
    The task loop for managing the connection to Cemu.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: The Wind Waker HD client context.
    """
    global TWWHDMemory
    logger.info("Starting Cemu connector. Use /cemu for status information.")
    sleep_time = 0.0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                # ctx.watcher_event gets set when receiving ReceivedItems or LocationInfo, or when shutting down.
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except asyncio.TimeoutError:
                pass
            sleep_time = 0.0
        ctx.watcher_event.clear()

        try:
            if TWWHDMemory and ctx.cemu_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame(ctx):
                    # Reset the give item array while not in the game.
                    sleep_time = 0.1
                    continue
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                    await check_current_stage_changed(ctx)
                else:
                    if not ctx.auth:
                        await ctx.get_username()
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                sleep_time = 0.1
            else:
                if ctx.cemu_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Cemu lost, reconnecting...")
                    ctx.cemu_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Cemu...")
                try:
                    TWWHDMemory = pymem.Pymem("Cemu")
                    logger.info(CONNECTION_CONNECTED_STATUS)
                    ctx.cemu_status = CONNECTION_CONNECTED_STATUS
                    ctx.locations_checked = set()
                except Exception as e:
                    logger.info("Connection to Cemu failed, attempting again in 5 seconds...")
                    ctx.cemu_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    sleep_time = 5
                    continue
                    
        except Exception:
            TWWHDMemory=None
            logger.info("Connection to Cemu failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.cemu_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            sleep_time = 5
            continue


def main(*args: str) -> None:
    """
    Run the main async loop for the Wind Waker HD client.

    :param *args: Command line arguments passed to the client.
    """
    Utils.init_logging("The Wind Waker HD Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = TWWHDContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        await ctx.exit_event.wait()
        # Wake the sync task, if it is currently sleeping, so it can start shutting down when it sees that the
        # exit_event is set.
        ctx.watcher_event.set()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.cemu_sync_task:
            await ctx.cemu_sync_task

    parser = get_base_parser()
    parsed_args = parser.parse_args(args)

    import colorama

    colorama.init()
    asyncio.run(_main(parsed_args.connect, parsed_args.password))
    colorama.deinit()

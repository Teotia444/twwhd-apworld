import asyncio
from asyncio.log import logger
import sys
import time
import traceback
from typing import Optional
import pymem

from ..TWWHDClient import TWWHDContext
from ..Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from ..Locations import ISLAND_NAME_TO_SALVAGE_BIT, LOCATION_TABLE, TWWHDLocation, TWWHDLocationData, TWWHDLocationType
from ..randomizers.Charts import ISLAND_NUMBER_TO_NAME

from NetUtils import ClientStatus


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


if sys.platform != "win32":
    import struct

    class LinuxMemory:
        def __init__(self, process_name: str):
            self.pid = self._find_pid(process_name)
            self._mem_path = f"/proc/{self.pid}/mem"
        
        def _find_pid(self, process_name: str) -> int:
            for pid in os.listdir("/proc"):
                if pid.isdigit():
                    try:
                        with open(f"/proc/{pid}/comm") as f:
                            if process_name.lower() in f.read().strip().lower():
                                return int(pid)
                    except (FileNotFoundError, PermissionError):
                        pass
            raise ProcessLookupError(f"Process '{process_name}' not found")

        def _read(self, address: int, length: int) -> bytes:
            with open(self._mem_path, "rb") as f:
                f.seek(address)
                return f.read(length)

        def _write(self, address: int, data: bytes) -> None:
            with open(self._mem_path, "rb+") as f:
                f.seek(address)
                f.write(data)


        def read_bytes(self, address: int, length: int) -> bytes:
            return self._read(address, length)

        def read_long(self, address: int) -> int:
            return struct.unpack("i", self._read(address, 4))[0]

        def read_short(self, address: int) -> int:
            return struct.unpack("H", self._read(address, 2))[0]

        def read_uchar(self, address: int) -> int:
            return struct.unpack("B", self._read(address, 1))[0]

        def read_bool(self, address: int) -> bool:
            return bool(self.read_uchar(address))

        def read_string(self, address: int, length: int) -> str:
            return self._read(address, length).split(b"\x00")[0].decode("utf-8", errors="ignore")

        def write_short(self, address: int, value: int) -> None:
            self._write(address, struct.pack("H", value))

        def write_uchar(self, address: int, value: int) -> None:
            self._write(address, struct.pack("B", value))

        def write_long(self, address: int, value: int) -> None:
            self._write(address, struct.pack("i", value))

        def write_bytes(self, address: int, data: bytes, length: int = None) -> None:
            self._write(address, data)


# This address is used to check/set the player's health for DeathLink.
CURR_HEALTH_ADDR = 0x145b7b82

M_MODE_ADDR = 0x10474342

# These addresses are used for the Moblin's Letter check.
LETTER_BASE_ADDR = 0x145B7C06
LETTER_OWND_ADDR = 0x145B7C10

# These addresses are used to check flags for locations.
CHARTS_BITFLD_ADDR = 0x145B7C74
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

# This address points to the story flags array
STORY_FLAGS_ARR_ADDR = 0x145B81A4

# This address is used to check the stage name to verify that the player is in-game before sending items.
CURR_STAGE_NAME_ADDR = 0x104741F0

# This address is the start of an array that we use to inform us of which charts lead where.
# The array is of length 49, and each element is two bytes. The index represents the chart's original destination, and
# the value represents the new destination.
# The chart name is inferrable from the chart's original destination.
CHARTS_MAPPING_ADDR = 0x803FE8E0

ITEM_GET_BYTE_ADDR = 0x28F8844

if sys.platform == "win32":
    MemoryType = pymem.Pymem
else:
    MemoryType = LinuxMemory

TWWHDMemory: Optional[MemoryType] = None


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

def read_uchar(ctx:TWWHDContext, console_address: int) -> str:
    """
    Read a single byte char from Cemu memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    global TWWHDMemory
    return TWWHDMemory.read_uchar(ctx.CEMU_BASE_ADDR+console_address)

def write_uchar(ctx:TWWHDContext, console_address: int, value: int) -> str:
    """
    Write a single byte to Cemu memory.
        
    :param console_address: Address to write to.
    :param value: Value to write.
    """
    global TWWHDMemory
    return TWWHDMemory.write_uchar(ctx.CEMU_BASE_ADDR+console_address, value)

def read_long(ctx:TWWHDContext, console_address: int) -> str:
    """
    Read a 4-byte long from Cemu memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    global TWWHDMemory
    return TWWHDMemory.read_long(ctx.CEMU_BASE_ADDR+console_address)

def read_bytes(ctx:TWWHDContext, console_address: int, len:int) -> str:
    """
    Read a specified byte count from Cemu memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    global TWWHDMemory
    return TWWHDMemory.read_bytes(ctx.CEMU_BASE_ADDR+console_address, len)

def _give_death(ctx: TWWHDContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: The Wind Waker HD client context.
    """
    global TWWHDMemory
    if (
        ctx.slot is not None
        and TWWHDMemory is not None
        and ctx.status == CONNECTION_CONNECTED_STATUS
        and check_ingame(ctx)
    ):
        ctx.has_send_death = True
        write_short(ctx, CURR_HEALTH_ADDR, 0)

def default_give_item(ctx:TWWHDContext, id:int):
    b = write_uchar(ctx, ITEM_GET_BYTE_ADDR, id) 
    return b

def _give_item(ctx: TWWHDContext, item_name: str) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The Wind Waker client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    if not check_ingame(ctx) or not (read_uchar(ctx, ITEM_GET_BYTE_ADDR) == 0xFF):
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
            if(read_uchar(ctx, LETTER_BASE_ADDR + i) == 0x98): #fathers letter id
                write_uchar(ctx, LETTER_BASE_ADDR + i, 0xFF)

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
    if location_name == "Windfall Island - Lenzo Become Assistant":
        checked = (
            read_uchar(ctx, STORY_FLAGS_ARR_ADDR + data.address) & 0x6 == 0x6
            or read_uchar(ctx, STORY_FLAGS_ARR_ADDR + data.address) & 0x7 == 0x7
        )

    # The "Windfall Island - Maggie - Delivery Reward" flag remains unknown.
    # However, as a temporary workaround, we can check if the player had Moblin's letter at some point, but it's no
    # longer in their Delivery Bag.
    elif location_name == "Windfall Island - Maggie Delivery Reward":
        was_moblins_owned = (read_long(ctx, LETTER_OWND_ADDR) >> 23) & 1
        dbag_contents : list[int] = [read_uchar(ctx, LETTER_BASE_ADDR + offset) for offset in range(8)]
        checked = was_moblins_owned and 0x9B not in dbag_contents

    # For Letter from Hoskit's Girlfriend, we need to check two bytes.
    # 0x1 = Golden Feathers delivered, 0x2 = Mail sent by Hoskit's Girlfriend, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Hoskit's Girlfriend":
        checked = read_uchar(ctx, STORY_FLAGS_ARR_ADDR + data.address) & 0x3 == 0x3

    # For Letter from Baito's Mother, we need to check two bytes.
    # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Baito's Mother":
        checked = read_uchar(ctx, STORY_FLAGS_ARR_ADDR + data.address) & 0x3 == 0x3

    # For Letter from Grandma, we need to check two bytes.
    # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Grandma":
        checked = read_uchar(ctx, STORY_FLAGS_ARR_ADDR + data.address) & 0x3 == 0x3

    else:
        raise NotImplementedError(f"Unknown special location: {location_name}")

    return checked

async def check_locations(ctx: TWWHDContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: The Wind Waker client context.
    """
    # Read the bitfield for sunken treasure locations.
    ctx.charts_bitfield = int.from_bytes(read_bytes(ctx, CHARTS_BITFLD_ADDR, 8), byteorder="big")

    # Read the bitfields once before the loop to speed things up a bit.
    ctx.chests_bitfields = {}
    ctx.switches_bitfields = {}
    ctx.pickups_bitfields = {}
    for stage_id in range(0xE):
        chest_bitfield_addr = BASE_CHESTS_BITFLD_ADDR + (0x24 * stage_id)
        switches_bitfield_addr = BASE_SWITCHES_BITFLD_ADDR + (0x24 * stage_id)
        pickups_bitfield_addr = BASE_PICKUPS_BITFLD_ADDR + (0x24 * stage_id)

        ctx.chests_bitfields[stage_id] = int.from_bytes(
            read_bytes(ctx, chest_bitfield_addr, 0x4), byteorder="big"
        )
        ctx.switches_bitfields[stage_id] = int.from_bytes(
            read_bytes(ctx, switches_bitfield_addr, 10), byteorder="big"
        )
        ctx.pickups_bitfields[stage_id] = int.from_bytes(
            read_bytes(ctx, pickups_bitfield_addr, 0x4), byteorder="big"
        )

    ctx.curr_stage_chests_bitfield = int.from_bytes(
        read_bytes(ctx, CURR_STAGE_CHESTS_BITFLD_ADDR, 0x4), byteorder="big"
    )
    ctx.curr_stage_switches_bitfield = int.from_bytes(
        read_bytes(ctx, CURR_STAGE_SWITCHES_BITFLD_ADDR, 10), byteorder="big"
    )
    ctx.curr_stage_pickups_bitfield = int.from_bytes(
        read_bytes(ctx, CURR_STAGE_PICKUPS_BITFLD_ADDR, 0x4), byteorder="big"
    )

    # We check which locations are currently checked on the current stage.
    curr_stage_id = read_short(ctx, CURR_STAGE_ID_ADDR)

    # Loop through all locations to see if each has been checked.
    for location, data in LOCATION_TABLE.items():
        checked = False
        if data.type == TWWHDLocationType.CHART:
            if location in ctx.salvage_locations_map: 
                salvage_bit = ctx.salvage_locations_map[location]
                checked = bool((ctx.charts_bitfield >> salvage_bit) & 1)
        elif data.type == TWWHDLocationType.BOCTO:
            assert data.address is not None
            checked = bool((read_uchar(ctx, STORY_FLAGS_ARR_ADDR + 1 + data.address) >> data.bit) & 1)
        elif data.type == TWWHDLocationType.EVENT:
            checked = bool((read_uchar(ctx, STORY_FLAGS_ARR_ADDR + data.address) >> data.bit) & 1)
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
        m_mode = read_short(ctx, M_MODE_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3 and m_mode == 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False


def check_ingame(ctx: TWWHDContext) -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    if ctx.CEMU_BASE_ADDR == 0 :
        return False
    return read_string(ctx, CURR_STAGE_NAME_ADDR, 8) not in ["", "sea_T", "Name"]


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
            if TWWHDMemory and ctx.status == CONNECTION_CONNECTED_STATUS:
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
                if ctx.status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Cemu lost, reconnecting...")
                    ctx.status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Cemu...")
                try:
                    TWWHDMemory = pymem.Pymem("Cemu") if sys.platform == "win32" else LinuxMemory("Cemu")
                    logger.info(CONNECTION_CONNECTED_STATUS)
                    ctx.status = CONNECTION_CONNECTED_STATUS
                    ctx.locations_checked = set()
                except Exception as e:
                    logger.info("Connection to Cemu failed, attempting again in 5 seconds...")
                    ctx.status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    sleep_time = 5
                    continue
                    
        except Exception:
            TWWHDMemory=None
            ctx.CEMU_BASE_ADDR = 0
            logger.info("Connection to Cemu failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            sleep_time = 5
            continue
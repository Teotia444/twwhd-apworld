import asyncio
from CommonClient import logger
import json
import socket
import struct
import time
import traceback
from typing import Optional

from NetUtils import ClientStatus

from ..Locations import LOCATION_TABLE, TWWHDLocation, TWWHDLocationData, TWWHDLocationType
from ..Items import ITEM_TABLE, LOOKUP_ID_TO_NAME
from ..TWWHDClient import TWWHDContext


CONNECTION_REFUSED_GAME_STATUS = (
    "Wii U failed to connect. Please load a randomized ROM for The Wind Waker HD. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Wii U failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Wii U connection was lost. Please make sure The Wind Waker HD is running and the AP helper is installed."
)
CONNECTION_CONNECTED_STATUS = "Wii U connected successfully."
CONNECTION_INITIAL_STATUS = "Wii U connection has not been initiated."


class WiiUClass:
    def __init__(self, _ip_addr: str):
        self.ip_addr = _ip_addr
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_addr, 3599))

        self.chest_bitfield: Optional[list[list[int]]] = None
        self.switches_bitfield: Optional[list[list[int]]] = None
        self.pickups_bitfield: Optional[list[list[int]]] = None

        self.curr_stage_chests_bitfield: Optional[list[list[int]]] = None
        self.curr_stage_switches_bitfield: Optional[list[list[int]]] = None
        self.curr_stage_pickups_bitfield: Optional[list[list[int]]] = None

        self.charts_bitfield: Optional[list[int]] = None
        self.story_flags: Optional[list[int]] = None
        self.octo_flags: Optional[list[int]] = None

        self.mMode: Optional[int] = None
        self.curr_stage_idx: Optional[int] = None
        self.health: Optional[int] = None
        self.itemGetVal: Optional[int] = None
        self.expectedIdx: Optional[int] = None

        self.stage_name: str = ""
        self.dBag_content: Optional[list[int]] = None
        self.dBag_flags: Optional[list[int]] = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_addr, 3599))

    def recv_num(self, n: int):
        data = bytearray()
        while len(data) < n :
            chunk = self.socket.recv(n-len(data))
            if not chunk:
                raise ConnectionError("Connection to the Wii U was closed while receiving data")
            data.extend(chunk)
        return bytes(data)

    def recv(self):
        # start with the header
        header = self.recv_num(4)
        length = struct.unpack("!I", header)[0]
        return self.recv_num(length)

    def send(self, payload:str):
        self.socket.send(payload.encode())
        res = self.recv()
        if not res:
            raise ConnectionError("Recieved nothing from the Wii U!")
        return json.loads(res)

    def update(self):
        data = self.send("u")
        if data["result"] != 0:
            return False
        self.chest_bitfield = data["data"]["chest_bitfields"]
        self.switches_bitfield = data["data"]["switches_bitfields"] 
        for i in range(len(self.switches_bitfield)):
            self.switches_bitfield[i] = self.switches_bitfield[i][:10] # this is really dumb
        
        self.pickups_bitfield = data["data"]["pickups_bitfields"]

        self.curr_stage_chests_bitfield = data["data"]["current_chest_bitfield"]
        self.curr_stage_switches_bitfield = data["data"]["current_switch_bitfield"][:10] #same as above


        self.curr_stage_pickups_bitfield = data["data"]["current_pickup_bitfield"]

        self.charts_bitfield = data["data"]["charts_bitfield"]
        self.story_flags = data["data"]["story_flags"]
        self.octo_flags = data["data"]["octo_flags"]

        self.mMode = data["data"]["mMode"]
        self.curr_stage_idx = data["data"]["curr_stage_idx"]
        self.stage_name = data["data"]["curr_stage_name"]
        self.health = data["data"]["health"]
        self.itemGetVal = data["data"]["itemGetVal"]
        self.expectedIdx = data["data"]["expectedIdx"]
        self.dBag_content = data["data"]["dBag_content"]
        self.dBag_flags = data["data"]["dBag_flags"]


TWWHDMemory: Optional[WiiUClass] = None

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
    ):
        res = TWWHDMemory.send("h0")
        if res["result"] != 0:
            return
        ctx.has_send_death = True

def _give_item(ctx: TWWHDContext, item_name: str) -> bool:
    """
    Give an item to the player in-game.

    :param ctx: The Wind Waker client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    global TWWHDMemory
    res = TWWHDMemory.send("g" + str(ITEM_TABLE[item_name].item_id))
    return res["result"]

async def give_items(ctx: TWWHDContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: The Wind Waker HD client context.
    """
    global TWWHDMemory
    # Read the expected index of the player, which is the index of the next item they're expecting to receive.
    # The expected index starts at 0 for a fresh save file.
    expected_idx = TWWHDMemory.expectedIdx
    # Check if there are new items.
    received_items = ctx.items_received
    if len(received_items) <= expected_idx:
        # There are no new items.
        return
    # Loop through items to give.
    # Give the player all items at an index greater than or equal to the expected index.
    for idx, item in enumerate(received_items[expected_idx:], start=expected_idx):
        # Attempt to give the item and increment the expected index.
        res = _give_item(ctx, LOOKUP_ID_TO_NAME[item.item])
        while not res == 0:
            await asyncio.sleep(0.01)
            res = _give_item(ctx, LOOKUP_ID_TO_NAME[item.item])
            if res == 2:
                return
        # if(item.player == 0):
        #     TWWHDMemory.send("nRecieved " + str(LOOKUP_ID_TO_NAME[item.item]) + " from the server!")
        # elif(item.player != ctx.slot):
        #     TWWHDMemory.send("nRecieved " + str(LOOKUP_ID_TO_NAME[item.item]) + " from " + ctx.player_names[item.player] + " !")    
        # Increment the expected index.
        TWWHDMemory.send("i1")

def check_special_location(ctx:TWWHDContext, location_name: str, data: TWWHDLocationData) -> bool:
    """
    Check that the player has checked a given location.
    This function handles locations that require special logic.

    :param location_name: The name of the location.
    :param data: The data associated with the location.
    :raises NotImplementedError: If an unknown location name is provided.
    """
    global TWWHDMemory
    checked = False

    # For "Windfall Island - Lenzo's House - Become Lenzo's Assistant"
    # 0x6 is delivered the final picture for Lenzo, 0x7 is a day has passed since becoming his assistant
    # Either is fine for sending the check, so check both conditions. TODO
    if location_name == "Windfall Island - Lenzo Become Assistant":
        checked = (
            TWWHDMemory.story_flags[data.address] & 0x6 == 0x6
            or TWWHDMemory.story_flags[data.address] & 0x7 == 0x7
        )

    # The "Windfall Island - Maggie - Delivery Reward" flag remains unknown.
    # However, as a temporary workaround, we can check if the player had Moblin's letter at some point, but it's no
    # longer in their Delivery Bag.
    elif location_name == "Windfall Island - Maggie Delivery Reward":
        was_moblins_owned = TWWHDMemory.dBag_flags[2] & 0x80 == 0x80 
        checked = was_moblins_owned and 0x9B not in TWWHDMemory.dBag_content

    # For Letter from Hoskit's Girlfriend, we need to check two bytes.
    # 0x1 = Golden Feathers delivered, 0x2 = Mail sent by Hoskit's Girlfriend, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Hoskit's Girlfriend":
        checked = TWWHDMemory.story_flags[data.address] & 0x3 == 0x3

    # For Letter from Baito's Mother, we need to check two bytes.
    # 0x1 = Note to Mom sent, 0x2 = Mail sent by Baito's Mother, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Baito's Mother":
        checked = TWWHDMemory.story_flags[data.address] & 0x3 == 0x3

    # For Letter from Grandma, we need to check two bytes.
    # 0x1 = Grandma saved, 0x2 = Mail sent by Grandma, 0x3 = Mail read by Link
    elif location_name == "Mailbox - Letter from Grandma":
        checked = TWWHDMemory.story_flags[data.address] & 0x3 == 0x3

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
    global TWWHDMemory
    # Read the bitfield for sunken treasure locations.
    ctx.charts_bitfield = int.from_bytes(bytes(TWWHDMemory.charts_bitfield), byteorder="big")

    # Read the bitfields once before the loop to speed things up a bit.
    ctx.chests_bitfields = {}
    ctx.switches_bitfields = {}
    ctx.pickups_bitfields = {}
    for stage_id in range(0xE):

        ctx.chests_bitfields[stage_id] = int.from_bytes(
            bytes(TWWHDMemory.chest_bitfield[stage_id]), byteorder="big"
        )
        ctx.switches_bitfields[stage_id] = int.from_bytes(
            bytes(TWWHDMemory.switches_bitfield[stage_id]), byteorder="big"
        )
        ctx.pickups_bitfields[stage_id] = int.from_bytes(
            bytes(TWWHDMemory.pickups_bitfield[stage_id]), byteorder="big"
        )

    ctx.curr_stage_chests_bitfield = int.from_bytes(
        bytes(TWWHDMemory.curr_stage_chests_bitfield), byteorder="big"
    )
    ctx.curr_stage_switches_bitfield = int.from_bytes(
        bytes(TWWHDMemory.curr_stage_switches_bitfield), byteorder="big"
    )
    ctx.curr_stage_pickups_bitfield = int.from_bytes(
        bytes(TWWHDMemory.curr_stage_pickups_bitfield), byteorder="big"
    )

    # We check which locations are currently checked on the current stage.
    curr_stage_id = TWWHDMemory.curr_stage_idx

    # Loop through all locations to see if each has been checked.
    for location, data in LOCATION_TABLE.items():
        checked = False
        if data.type == TWWHDLocationType.CHART:
            if location in ctx.salvage_locations_map: 
                salvage_bit = ctx.salvage_locations_map[location]
                checked = bool((ctx.charts_bitfield >> salvage_bit) & 1)
        elif data.type == TWWHDLocationType.BOCTO:
            assert data.address is not None
            checked = bool((TWWHDMemory.octo_flags[101 + data.address] >> data.bit) & 1)
        elif data.type == TWWHDLocationType.EVENT:
            checked = bool((TWWHDMemory.story_flags[data.address] >> data.bit) & 1)
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
    global TWWHDMemory
    new_stage_name = TWWHDMemory.stage_name

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
    global TWWHDMemory
    return TWWHDMemory.health > 0 

async def check_death(ctx: TWWHDContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    global TWWHDMemory
    if ctx.slot is not None and check_ingame(ctx):
        cur_health = TWWHDMemory.health
        m_mode = TWWHDMemory.mMode
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
    global TWWHDMemory
    if TWWHDMemory.socket == None :
        return False
    return TWWHDMemory.stage_name not in ["", "sea_T", "Name"]

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

def _forward_message_func(ctx: TWWHDContext, data):
    global TWWHDMemory
    TWWHDMemory.send("n"+data)

async def wiiu_sync_task(ctx: TWWHDContext) -> None:
    """
    The task loop for managing the connection to the Wii U.

    While connected, read the socket to look for any relevant changes made by the player in the game.

    :param ctx: The Wind Waker HD client context.
    """
    global TWWHDMemory
    logger.info("Starting Wii U connector. Use /wiiu for status information.")
    ctx.give_death_func = _give_death
    ctx.forward_message_func = _forward_message_func
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
                TWWHDMemory.update()
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
                    logger.info("Connection to the Wii U lost, reconnecting...")
                    ctx.status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to the Wii U...")
                try:
                    TWWHDMemory.connect()
                    logger.info(CONNECTION_CONNECTED_STATUS)
                    ctx.status = CONNECTION_CONNECTED_STATUS
                    ctx.locations_checked = set()
                except Exception as e:
                    logger.info("Connection to the Wii U failed, attempting again in 5 seconds...")
                    ctx.status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    sleep_time = 5
                    continue
                    
        except Exception:
            TWWHDMemory.socket = None
            logger.info("Connection to the Wii U failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            sleep_time = 5
            continue

def setup_wiiu_mem(ip: str):
    global TWWHDMemory
    TWWHDMemory = WiiUClass(ip)
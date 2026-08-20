import asyncio
import copy
import os

from typing import TYPE_CHECKING, Any, Optional

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop

from .Locations import ISLAND_NAME_TO_SALVAGE_BIT
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

# Data storage key
AP_VISITED_STAGE_NAMES_KEY_FORMAT = "twwhd_visited_stages_%i"


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

    async def _cmd_cemu(self) -> None:
        """
        Connects the client to Cemu.
        Display the current Cemu emulator connection status if the client is already connected.
        """

        if isinstance(self.ctx, TWWHDContext) and self.ctx.auth and self.ctx.sync_task is None:
            if os.path.isfile(os.getenv('APPDATA') + "\\Cemu\\log.txt"):
                with open(os.getenv('APPDATA') + "\\Cemu\\log.txt") as f:
                    next(f)
                    base_addr = "0x" + f.readline().split("0x")[1].split(")")[0]
                    self.ctx.CEMU_BASE_ADDR = int(base_addr, base=16)
                    
            else:
                logger.info('Enter base address:')
                base_addr = await self.ctx.console_input()
                self.ctx.CEMU_BASE_ADDR = int(base_addr, base=16)

            from .helpers.Cemu import cemu_sync_task
            self.ctx.sync_task = asyncio.create_task(cemu_sync_task(self.ctx), name="CemuSync")
            logger.info('Cemu is connected!')

        elif isinstance(self.ctx, TWWHDContext) and not self.ctx.auth:
            logger.info(f"Connect to the AP room before connecting to Cemu!")

        elif isinstance(self.ctx, TWWHDContext):
            logger.info(f"Cemu Status: {self.ctx.status}")
        
    async def _cmd_wiiu(self, ip_addr: str) -> None:
        """
        Connects the client to the Wii U.
        Display the current Wii U connection status if the client is already connected.
        """

        if isinstance(self.ctx, TWWHDContext) and self.ctx.auth and self.ctx.sync_task is None:
            from .helpers.WiiU import wiiu_sync_task, setup_wiiu_mem
            setup_wiiu_mem(ip_addr)
            self.ctx.sync_task = asyncio.create_task(wiiu_sync_task(self.ctx), name="WiiUSync")
            logger.info('Wii U is connected!')

        elif isinstance(self.ctx, TWWHDContext) and not self.ctx.auth:
            logger.info(f"Connect to the AP room before connecting to the Wii U!")

        elif isinstance(self.ctx, TWWHDContext):
            logger.info(f"Wii U Status: {self.ctx.status}")


    def _cmd_attach(self, base_addr: str) -> None:
        """
        Deprecated

        :param base_addr: The base cemu address.
        """
        logger.info(f"Deprecated command! Your client should already be connected. Use /cemu to check the status of your connection.")

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
        self.sync_task: Optional[asyncio.Task[None]] = None
        self.status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.has_send_death: bool = False
        self.give_death_func: Optional[function] = None
        self.forward_message_func: Optional[function] = None

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
            # if os.path.isfile(os.getenv('APPDATA') + "\\Cemu\\log.txt"):
            #     with open(os.getenv('APPDATA') + "\\Cemu\\log.txt") as f:
            #         next(f)
            #         base_addr = "0x" + f.readline().split("0x")[1].split(")")[0]
            #         self.CEMU_BASE_ADDR = int(base_addr, base=16)
            #         
            # else:
            #     logger.info('Enter base address:')
            #     base_addr = await self.console_input()
            #     self.CEMU_BASE_ADDR = int(base_addr, base=16)
            #     
            # self.cemu_sync_task = asyncio.create_task(cemu_sync_task(self), name="CemuSync")
            

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
        self.give_death_func(self)

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

    def on_print_json(self, args: dict) -> None:
        if not self.is_uninteresting_item_send(args) and self.forward_message_func:
            self.forward_message_func(self, self.rawjsontotextparser(copy.deepcopy(args["data"])))

        super().on_print_json(args)

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

        if ctx.sync_task:
            await ctx.sync_task

    parser = get_base_parser()
    parsed_args = parser.parse_args(args)

    import colorama

    colorama.init()
    asyncio.run(_main(parsed_args.connect, parsed_args.password))
    colorama.deinit()

# flake8: noqa

from collections.abc import Callable
from typing import TYPE_CHECKING

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule

from .Macros import *

if TYPE_CHECKING:
    from . import TWWHDWorld


class TWWHDLogic(LogicMixin):
    """
    This class implements some of the game logic for The Wind Waker HD.

    This class's methods reference the world's options. All methods defined in this class should be prefixed with
    "_twwhd."
    """

    multiworld: MultiWorld

    def _twwhd_has_chart_for_island(self, player: int, island_number: int) -> bool:
        chart_item_name = self.multiworld.worlds[player].charts.island_number_to_chart_name[island_number]

        if "Triforce Chart" in chart_item_name:
            return self.has(chart_item_name, player) and has_any_wallet_upgrade(self, player)
        else:
            return self.has(chart_item_name, player)

    def _twwhd_can_defeat_all_required_bosses(self, player: int) -> bool:
        required_boss_item_locations = self.multiworld.worlds[player].boss_reqs.required_boss_item_locations
        for loc in required_boss_item_locations:
            if not self.can_reach_location(loc, player):
                return False
        return True

    def _twwhd_rematch_bosses_skipped(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_rematch_bosses_skipped

    def _twwhd_in_swordless_mode(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_in_swordless_mode

    def _twwhd_outside_swordless_mode(self, player: int) -> bool:
        return not self.multiworld.worlds[player].logic_in_swordless_mode

    def _twwhd_in_required_bosses_mode(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_in_required_bosses_mode

    def _twwhd_outside_required_bosses_mode(self, player: int) -> bool:
        return not self.multiworld.worlds[player].logic_in_required_bosses_mode

    def _twwhd_obscure_1(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_obscure_1

    def _twwhd_obscure_2(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_obscure_2

    def _twwhd_obscure_3(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_obscure_3

    def _twwhd_precise_1(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_precise_1

    def _twwhd_precise_2(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_precise_2

    def _twwhd_precise_3(self, player: int) -> bool:
        return self.multiworld.worlds[player].logic_precise_3

def set_rules(world: "TWWHDWorld") -> None:  # noqa: F405
    """
    Define the logic rules for locations in The Wind Waker HD.
    Rules are only set for locations if they are present in the world.

    :param world: The Wind Waker HD game world.
    """

    def set_rule_if_exists(location_name: str, rule: Callable[[CollectionState], bool]) -> None:
        if location_name in world.progress_locations:
            set_rule(world.get_location(location_name), rule)

    player = world.player

    # Outset Island
    set_rule_if_exists("Outset Island - Under Link's House", lambda state: True)
    set_rule_if_exists("Outset Island - Mesa's House Chest", lambda state: True)
    set_rule_if_exists(
        "Outset Island - Orca Give 10 Knight's Crests",
        lambda state: state.has("Spoils Bag", player)
        and can_sword_fight_with_orca(state, player)
        and has_magic_meter(state, player)
        and can_farm_knights_crests(state, player),
    )
    # set_rule_if_exists("Outset Island - Orca - Hit 500 Times", lambda state: can_sword_fight_with_orca(state, player))
    set_rule_if_exists(
        "Outset Island - Great Fairy", lambda state: state.can_reach_region("Outset Fairy Fountain", player)
    )
    set_rule_if_exists("Jabun's Cave Chest", lambda state: state.has("Bombs", player))
    set_rule_if_exists(
        "Outset Island - Dig up Black Soil", lambda state: state.has_all(["Bait Bag", "Power Bracelets"], player)
    )
    set_rule_if_exists(
        "Outset Island - Savage Labyrinth Floor 30",
        lambda state: can_defeat_keese(state, player)
        and can_defeat_miniblins(state, player)
        and can_defeat_red_chuchus(state, player)
        and can_defeat_magtails(state, player)
        and can_defeat_fire_keese(state, player)
        and can_defeat_peahats(state, player)
        and can_defeat_green_chuchus(state, player)
        and can_defeat_boko_babas(state, player)
        and can_defeat_mothulas(state, player)
        and can_defeat_winged_mothulas(state, player)
        and can_defeat_wizzrobes(state, player)
        and can_defeat_armos(state, player)
        and can_defeat_yellow_chuchus(state, player)
        and can_defeat_red_bubbles(state, player)
        and can_defeat_darknuts(state, player)
        and can_play_winds_requiem(state, player)
        and (state.has_any(["Grappling Hook", "Skull Hammer"], player) or has_heros_sword(state, player)),
    )
    set_rule_if_exists(
        "Outset Island - Savage Labyrinth Floor 50",
        lambda state: can_defeat_keese(state, player)
        and can_defeat_miniblins(state, player)
        and can_defeat_red_chuchus(state, player)
        and can_defeat_magtails(state, player)
        and can_defeat_fire_keese(state, player)
        and can_defeat_peahats(state, player)
        and can_defeat_green_chuchus(state, player)
        and can_defeat_boko_babas(state, player)
        and can_defeat_mothulas(state, player)
        and can_defeat_winged_mothulas(state, player)
        and can_defeat_wizzrobes(state, player)
        and can_defeat_armos(state, player)
        and can_defeat_yellow_chuchus(state, player)
        and can_defeat_red_bubbles(state, player)
        and can_defeat_darknuts(state, player)
        and can_play_winds_requiem(state, player)
        and (state.has_any(["Grappling Hook", "Skull Hammer"], player) or has_heros_sword(state, player))
        and can_aim_mirror_shield(state, player)
        and can_defeat_redeads(state, player)
        and can_defeat_blue_bubbles(state, player)
        and can_defeat_stalfos(state, player)
        and state.has("Skull Hammer", player),
    )

    # Windfall Island
    set_rule_if_exists("Windfall Island - Tingle First Gift", lambda state: True)
    set_rule_if_exists("Windfall Island - Tingle Second Gift", lambda state: True)
    set_rule_if_exists("Windfall Island - Windfall Jail Maze Chest", lambda state: True)
    set_rule_if_exists(
        "Windfall Island - Chu Jelly Juice Shop - Potion Shop 15 Green Chu",
        lambda state: can_farm_green_chu_jelly(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Chu Jelly Juice Shop - Potion Shop 15 Blue Chu",
        lambda state: can_obtain_15_blue_chu_jelly(state, player),
    )
    set_rule_if_exists("Windfall Island - Ivan Catch Killer Bees", lambda state: True)
    set_rule_if_exists("Windfall Island - Mrs. Marie Catch Killer Bees", lambda state: True)
    set_rule_if_exists(
        "Windfall Island - Mrs. Marie 1 Joy Pendant",
        # In Archipelago, the non-randomized Joy Pendant on Windfall is not obtainable, so require the player to have
        # a way to collect Joy Pendants.
        lambda state: state.has("Spoils Bag", player) and can_farm_joy_pendants(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Mrs. Marie 21 Joy Pendant",
        lambda state: state.has("Spoils Bag", player) and can_farm_joy_pendants(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Mrs. Marie 40 Joy Pendant",
        lambda state: state.has("Spoils Bag", player) and can_farm_joy_pendants(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Lenzo House Left Chest",
        lambda state: can_play_winds_requiem(state, player) and has_picto_box(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Lenzo House Right Chest",
        lambda state: can_play_winds_requiem(state, player) and has_picto_box(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Lenzo Become Assistant", lambda state: has_picto_box(state, player)
    )
    set_rule_if_exists(
        "Windfall Island - Lenzo Bring Forest Firefly",
        lambda state: has_picto_box(state, player)
        and state.has("Empty Bottle", player)
        and can_access_forest_haven(state, player),
    )
    set_rule_if_exists("Windfall Island - House of Wealth Chest", lambda state: True)
    set_rule_if_exists(
        "Windfall Island - Maggie's Father Give 20 Skull Necklaces",
        lambda state: state.has("Spoils Bag", player) and can_farm_skull_necklaces(state, player),
    )
    set_rule_if_exists("Windfall Island - Maggie Free Item", lambda state: True)
    set_rule_if_exists(
        "Windfall Island - Maggie Delivery Reward",
        lambda state: state.has_all(["Delivery Bag", "Moblin's Letter"], player),
    )
    set_rule_if_exists(
        "Windfall Island - Cafe Postman Delivery", lambda state: state.has_all(["Delivery Bag", "Maggie's Letter"], player)
    )
    set_rule_if_exists(
        "Windfall Island - Kreeb Light the Lighthouse",
        lambda state: can_play_winds_requiem(state, player) and has_fire_arrows(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Transparent Chest",
        lambda state: can_play_winds_requiem(state, player)
        and has_fire_arrows(state, player)
        and (can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)),
    )
    set_rule_if_exists("Windfall Island - Tott Teach Rhythm", lambda state: state.has("Wind Waker", player))
    set_rule_if_exists("Windfall Island - Pirate Ship Chest", lambda state: True)
    set_rule_if_exists("Windfall Island - Auction 5 Rupee", lambda state: True)
    set_rule_if_exists("Windfall Island - Auction 40 Rupee", lambda state: True)
    set_rule_if_exists("Windfall Island - Auction 60 Rupee", lambda state: True)
    set_rule_if_exists("Windfall Island - Auction 80 Rupee", lambda state: True)
    set_rule_if_exists(
        "Windfall Island - Zunari Exotic Flower",
        lambda state: state.has("Delivery Bag", player),
    )
    set_rule_if_exists("Windfall Island - Sam Decorate Island", lambda state: state.has("Delivery Bag", player))
    # set_rule_if_exists(
    #     "Windfall Island - Kane - Place Shop Guru Statue on Gate", lambda state: state.has("Delivery Bag", player)
    # )
    # set_rule_if_exists(
    #     "Windfall Island - Kane - Place Postman Statue on Gate", lambda state: state.has("Delivery Bag", player)
    # )
    # set_rule_if_exists(
    #     "Windfall Island - Kane - Place Six Flags on Gate", lambda state: state.has("Delivery Bag", player)
    # )
    # set_rule_if_exists(
    #     "Windfall Island - Kane - Place Six Idols on Gate", lambda state: state.has("Delivery Bag", player)
    # )
    set_rule_if_exists("Windfall Island - Mila Catch Thief", lambda state: True)
    set_rule_if_exists("Windfall Island - Battle Squid First Prize", lambda state: True)
    set_rule_if_exists("Windfall Island - Battle Squid Second Prize", lambda state: True)
    set_rule_if_exists("Windfall Island - Battlesquid Under 20 Prize", lambda state: True)
    set_rule_if_exists(
        "Windfall Island - Pompie & Vera Secret Meeting Photo",
        lambda state: can_play_winds_requiem(state, player) and has_picto_box(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Kamo Full Moon Picture",
        lambda state: has_deluxe_picto_box(state, player) and can_play_song_of_passing(state, player),
    )
    set_rule_if_exists(
        "Windfall Island - Minenco Miss Windfall Picture", lambda state: has_deluxe_picto_box(state, player)
    )
    set_rule_if_exists(
        "Windfall Island - Linda and Anton",
        lambda state: has_deluxe_picto_box(state, player) and can_play_song_of_passing(state, player),
    )

    # Dragon Roost Island
    set_rule_if_exists("Dragon Roost Island - Wind Shrine", lambda state: state.has("Wind Waker", player))
    set_rule_if_exists(
        "Dragon Roost Island - Hoskit Give 20 Golden Feathers",
        lambda state: state.has("Spoils Bag", player) and can_farm_golden_feathers(state, player),
    )
    set_rule_if_exists(
        "Dragon Roost Island - Boulder Chest",
        lambda state: state.has_any(["Boomerang", "Bombs", "Bait Bag"], player) or has_heros_bow(state, player),
    )
    set_rule_if_exists(
        "Dragon Roost Island - Fly Across Platforms Around Island",
        lambda state: can_fly_with_deku_leaf_outdoors(state, player)
        and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player)),
    )
    set_rule_if_exists("Dragon Roost Island - Baito Mail Game", lambda state: True)
    set_rule_if_exists(
        "Dragon Roost Island - Cave Chest",
        lambda state: can_defeat_keese(state, player) and can_defeat_red_chuchus(state, player),
    )

    # Dragon Roost Cavern
    set_rule_if_exists("Dragon Roost Cavern - First Room Chest", lambda state: True)
    set_rule_if_exists(
        "Dragon Roost Cavern - Water Jug Alcove Chest", lambda state: state.has("Dragon Roost Cavern Small Key", player, 1)
    )
    set_rule_if_exists(
        "Dragon Roost Cavern - Water Jug on Upper Shelf", lambda state: state.has("Dragon Roost Cavern Small Key", player, 1)
    )
    set_rule_if_exists("Dragon Roost Cavern - Boarded Up Chest", lambda state: state.has("Dragon Roost Cavern Small Key", player, 1))
    set_rule_if_exists(
        "Dragon Roost Cavern - Swing Across Lava Chest",
        lambda state: state.has("Dragon Roost Cavern Small Key", player, 2)
        and (
            state.has("Grappling Hook", player)
            or can_fly_with_deku_leaf_indoors(state, player)
            or (state.has("Hookshot", player) and state._tww_obscure_1(player))
        ),
    )
    set_rule_if_exists("Dragon Roost Cavern - Rat Room Chest", lambda state: state.has("Dragon Roost Cavern Small Key", player, 2))
    set_rule_if_exists(
        "Dragon Roost Cavern - Rat Room Boarded Up Chest", lambda state: state.has("Dragon Roost Cavern Small Key", player, 2)
    )
    set_rule_if_exists("Dragon Roost Cavern - Bird's Nest", lambda state: state.has("Dragon Roost Cavern Small Key", player, 3))
    set_rule_if_exists("Dragon Roost Cavern - Dark Room Chest", lambda state: state.has("Dragon Roost Cavern Small Key", player, 4))
    set_rule_if_exists(
        "Dragon Roost Cavern - Pot on Upper Shelf in Pot Room", lambda state: state.has("Dragon Roost Cavern Small Key", player, 4)
    )
    set_rule_if_exists("Dragon Roost Cavern - Pot Room Chest", lambda state: state.has("Dragon Roost Cavern Small Key", player, 4))
    set_rule_if_exists("Dragon Roost Cavern - Mini Boss", lambda state: state.has("Dragon Roost Cavern Small Key", player, 4))
    set_rule_if_exists(
        "Dragon Roost Cavern - Under Rope Bridge Chest",
        lambda state: state.has("Dragon Roost Cavern Small Key", player, 4)
        and (state.has("Grappling Hook", player) or can_fly_with_deku_leaf_outdoors(state, player)),
    )
    set_rule_if_exists(
        "Dragon Roost Cavern - Tingle Statue Chest",
        lambda state: can_reach_dragon_roost_cavern_gaping_maw(state, player)
        and state.has("Grappling Hook", player)
        and has_tingle_bombs(state, player),
    )
    set_rule_if_exists(
        "Dragon Roost Cavern - Big Key Chest",
        lambda state: can_reach_dragon_roost_cavern_gaping_maw(state, player)
        and state.has("Grappling Hook", player)
        and can_stun_magtails(state, player),
    )
    set_rule_if_exists(
        "Dragon Roost Cavern - Boss Stairs Right Chest",
        lambda state: can_reach_dragon_roost_cavern_boss_stairs(state, player),
    )
    set_rule_if_exists(
        "Dragon Roost Cavern - Boss Stairs Left Chest",
        lambda state: can_reach_dragon_roost_cavern_boss_stairs(state, player),
    )
    set_rule_if_exists(
        "Dragon Roost Cavern - Boss Stairs Right Pot",
        lambda state: can_reach_dragon_roost_cavern_boss_stairs(state, player),
    )
    set_rule_if_exists("Dragon Roost Cavern - Gohma Heart Container", lambda state: can_defeat_gohma(state, player))

    # Forest Haven
    set_rule_if_exists(
        "Forest Haven - On Tree Branch",
        lambda state: can_access_forest_haven(state, player)
        and (
            state.has("Grappling Hook", player)
            or (
                can_fly_with_deku_leaf_indoors(state, player)
                and can_fly_with_deku_leaf_outdoors(state, player)
                and state._tww_obscure_1(player)
                and (
                    (can_cut_grass(state, player) and state._tww_precise_1(player))
                    or (has_magic_meter_upgrade(state, player) and state._tww_precise_2(player))
                )
            )
        ),
    )
    set_rule_if_exists(
        "Forest Haven - Chest on Small Island",
        lambda state: can_access_forest_haven(state, player)
        and (
            state.has("Grappling Hook", player)
            or (
                can_fly_with_deku_leaf_indoors(state, player)
                and can_fly_with_deku_leaf_outdoors(state, player)
                and state._tww_obscure_1(player)
                and (
                    (can_cut_grass(state, player) and state._tww_precise_1(player))
                    or (has_magic_meter_upgrade(state, player) and state._tww_precise_2(player))
                )
            )
        )
        and can_fly_with_deku_leaf_outdoors(state, player)
        and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player)),
    )

    # Forbidden Woods
    set_rule_if_exists("Forbidden Woods - First Room Chest", lambda state: True)
    set_rule_if_exists(
        "Forbidden Woods - Inside Hollow Tree Chest",
        lambda state: (can_defeat_door_flowers(state, player) or can_defeat_boko_babas(state, player)),
    )
    set_rule_if_exists(
        "Forbidden Woods - Boko Baba Climb Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player) and can_defeat_door_flowers(state, player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Pot High Above Hollow Tree", lambda state: can_fly_with_deku_leaf_indoors(state, player)
    )
    set_rule_if_exists(
        "Forbidden Woods - Hole in Tree Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player) and can_defeat_boko_babas(state, player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Morth Pit Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has("Grappling Hook", player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Vine Maze Left Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has("Grappling Hook", player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Vine Maze Right Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has("Grappling Hook", player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Highest Pot in Vine Maze",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has("Grappling Hook", player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Tall Room Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has_all(["Grappling Hook", "Forbidden Woods Small Key"], player)
        and (can_defeat_peahats(state, player) or state._tww_precise_2(player)),
    )
    set_rule_if_exists(
        "Forbidden Woods - Mothula Mini Boss Chest", lambda state: can_defeat_winged_mothulas(state, player)
    )
    set_rule_if_exists(
        "Forbidden Woods - Past Seeds Hanging by Vines Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has_all(["Grappling Hook", "Forbidden Woods Small Key"], player)
        and can_defeat_door_flowers(state, player)
        and (can_destroy_seeds_hanging_by_vines(state, player) or state._tww_precise_1(player)),
    )
    set_rule_if_exists(
        "Forbidden Woods - Chest Across Hanging Flower",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has_all(["Grappling Hook", "Boomerang"], player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Tingle Statue Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and state.has_all(["Grappling Hook", "Boomerang"], player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Locked Tree Trunk Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has_all(["Grappling Hook", "Boomerang"], player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Big Key Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has_all(["Grappling Hook", "Boomerang"], player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Double Mothula Room Chest",
        lambda state: can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and (can_defeat_door_flowers(state, player) or state.has("Grappling Hook", player))
        and can_defeat_mothulas(state, player),
    )
    set_rule_if_exists(
        "Forbidden Woods - Kalle Demos Heart Container", lambda state: can_defeat_kalle_demos(state, player)
    )

    # Greatfish Isle
    set_rule_if_exists("Greatfish Isle - Hidden Chest", lambda state: can_fly_with_deku_leaf_outdoors(state, player))

    # Tower of the Gods
    set_rule_if_exists("Tower of the Gods - Chest Behind Bombable Wall", lambda state: state.has("Bombs", player))
    set_rule_if_exists("Tower of the Gods - Pot Behind Bombable Wall", lambda state: state.has("Bombs", player))
    set_rule_if_exists("Tower of the Gods - Hop Across Floating Boxes Chest", lambda state: True)
    set_rule_if_exists("Tower of the Gods - Light Two Torches Chest", lambda state: state.has("Bombs", player))
    set_rule_if_exists("Tower of the Gods - Skull Room Chest", lambda state: state.has("Bombs", player))
    set_rule_if_exists(
        "Tower of the Gods - Shoot Eye Above Skulls Chest",
        lambda state: state.has("Bombs", player) and has_heros_bow(state, player),
    )
    set_rule_if_exists(
        "Tower of the Gods - Tingle Statue Chest",
        lambda state: can_reach_tower_of_the_gods_second_floor(state, player) and has_tingle_bombs(state, player),
    )
    set_rule_if_exists(
        "Tower of the Gods - First Armos Knights Chest",
        lambda state: can_reach_tower_of_the_gods_second_floor(state, player) and has_heros_bow(state, player),
    )
    set_rule_if_exists(
        "Tower of the Gods - Stone Tablet",
        lambda state: can_reach_tower_of_the_gods_second_floor(state, player) and state.has("Wind Waker", player),
    )
    set_rule_if_exists("Tower of the Gods - Darknut Mini Boss", lambda state: can_defeat_darknuts(state, player))
    set_rule_if_exists(
        "Tower of the Gods - Second Armos Knights Chest",
        lambda state: can_reach_tower_of_the_gods_second_floor(state, player)
        and state.has("Bombs", player)
        and can_play_winds_requiem(state, player),
    )
    set_rule_if_exists(
        "Tower of the Gods - Floating Platforms Room Lower Chest",
        lambda state: can_reach_tower_of_the_gods_second_floor(state, player)
        and (
            has_heros_bow(state, player)
            or (can_fly_with_deku_leaf_indoors(state, player) and state._tww_precise_1(player))
            or (state.has("Hookshot", player) and state._tww_obscure_1(player))
        ),
    )
    set_rule_if_exists(
        "Tower of the Gods - Floating Platforms Room Upper Chest",
        lambda state: can_reach_tower_of_the_gods_second_floor(state, player) and has_heros_bow(state, player),
    )
    set_rule_if_exists(
        "Tower of the Gods - Eastern Pot in Big Key Chest Room",
        lambda state: can_reach_tower_of_the_gods_third_floor(state, player),
    )
    set_rule_if_exists(
        "Tower of the Gods - Big Key Chest", lambda state: can_reach_tower_of_the_gods_third_floor(state, player)
    )
    set_rule_if_exists("Tower of the Gods - Gohdan Heart Container", lambda state: can_defeat_gohdan(state, player))

    # Hyrule
    set_rule_if_exists("Hyrule - Sword Chamber Chest", lambda state: can_defeat_mighty_darknuts(state, player))

    # Forsaken Fortress
    set_rule_if_exists(
        "Forsaken Fortress - Phantom Ganon", lambda state: can_reach_and_defeat_phantom_ganon(state, player)
    )
    set_rule_if_exists(
        "Forsaken Fortress - Chest Outside Upper Jail Cell",
        lambda state: can_get_inside_forsaken_fortress(state, player)
        and (
            can_fly_with_deku_leaf_indoors(state, player)
            or state.has("Hookshot", player)
            or state._tww_obscure_1(player)
        ),
    )
    set_rule_if_exists(
        "Forsaken Fortress - Chest Inside Lower Jail Cell",
        lambda state: can_get_inside_forsaken_fortress(state, player),
    )
    set_rule_if_exists(
        "Forsaken Fortress - Chest Guarded By Bokoblin", lambda state: can_get_inside_forsaken_fortress(state, player)
    )
    set_rule_if_exists(
        "Forsaken Fortress - Chest on Bed", lambda state: can_get_inside_forsaken_fortress(state, player)
    )
    set_rule_if_exists(
        "Forsaken Fortress - Helmaroc King Heart Container", lambda state: can_defeat_helmaroc_king(state, player)
    )

    # Mother and Child Isles
    set_rule_if_exists(
        "Mother & Child Isles - Inside Mother Isle", lambda state: can_play_ballad_of_gales(state, player)
    )

    # Fire Mountain
    set_rule_if_exists("Fire Mountain - Interior Chest", lambda state: can_defeat_magtails(state, player))
    set_rule_if_exists("Fire Mountain - Lookout Platform Chest", lambda state: True)
    set_rule_if_exists(
        "Fire Mountain - Lookout Platform Destroy Cannons", lambda state: can_destroy_cannons(state, player)
    )
    set_rule_if_exists(
        "Fire Mountain - Big Octo",
        lambda state: can_defeat_big_octos(state, player) and state.has("Grappling Hook", player),
    )

    # Ice Ring Isle
    set_rule_if_exists("Ice Ring Isle - Frozen Chest", lambda state: has_fire_arrows(state, player))
    set_rule_if_exists("Ice Ring Isle - Interior Chest", lambda state: True)
    set_rule_if_exists("Ice Ring Isle - Inner Cave Chest", lambda state: has_fire_arrows(state, player))

    # Headstone Island
    set_rule_if_exists("Headstone Island - Top of Island", lambda state: state.has("Bait Bag", player))
    set_rule_if_exists("Headstone Island - Submarine Chest", lambda state: can_defeat_bombchus(state, player))

    # Earth Temple
    set_rule_if_exists(
        "Earth Temple - Warp Pot Room Chest", lambda state: can_play_command_melody(state, player)
    )
    set_rule_if_exists(
        "Earth Temple - Warp Pot Room Behind Curtain",
        lambda state: can_play_command_melody(state, player)
        and has_fire_arrows(state, player)
        and state.has_any(["Boomerang", "Hookshot"], player),
    )
    set_rule_if_exists(
        "Earth Temple - First Crypt Chest",
        lambda state: can_reach_earth_temple_right_path(state, player)
        and state.has("Power Bracelets", player)
        and (can_play_command_melody(state, player) or has_mirror_shield(state, player)),
    )
    set_rule_if_exists(
        "Earth Temple - Chest Behind Destructible Wall",
        lambda state: can_reach_earth_temple_right_path(state, player) and has_mirror_shield(state, player),
    )
    set_rule_if_exists(
        "Earth Temple - Three Blocks Room Chest",
        lambda state: can_reach_earth_temple_left_path(state, player)
        and has_fire_arrows(state, player)
        and state.has("Power Bracelets", player)
        and can_defeat_floormasters(state, player)
        and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player)),
    )
    set_rule_if_exists(
        "Earth Temple - Behind Statues Chest",
        lambda state: can_reach_earth_temple_moblins_and_poes_room(state, player)
        and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player)),
    )
    set_rule_if_exists(
        "Earth Temple - Second Crypt Casket",
        lambda state: can_reach_earth_temple_moblins_and_poes_room(state, player),
    )
    set_rule_if_exists(
        "Earth Temple - Stalfos Mini Boss",
        lambda state: can_defeat_stalfos(state, player) or state.has("Hookshot", player),
    )
    set_rule_if_exists(
        "Earth Temple - Tingle Statue Chest",
        lambda state: can_reach_earth_temple_basement(state, player) and has_tingle_bombs(state, player),
    )
    set_rule_if_exists(
        "Earth Temple - Foggy Floormaster Room End Chest",
        lambda state: can_reach_earth_temple_redead_hub_room(state, player)
        and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player)),
    )
    set_rule_if_exists(
        "Earth Temple - Kill All Floormasters Chest",
        lambda state: can_reach_earth_temple_redead_hub_room(state, player)
        and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player))
        and can_defeat_floormasters(state, player),
    )
    set_rule_if_exists(
        "Earth Temple - Near Hammer Button Behind Curtain",
        lambda state: can_reach_earth_temple_redead_hub_room(state, player)
        and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player))
        and has_fire_arrows(state, player)
        and state.has_any(["Boomerang", "Hookshot"], player),
    )
    set_rule_if_exists(
        "Earth Temple - Third Crypt Chest", lambda state: can_reach_earth_temple_third_crypt(state, player)
    )
    set_rule_if_exists(
        "Earth Temple - Many Mirrors Room Right Chest",
        lambda state: can_reach_earth_temple_many_mirrors_room(state, player)
        and can_play_command_melody(state, player),
    )
    set_rule_if_exists(
        "Earth Temple - Many Mirrors Room Left Chest",
        lambda state: can_reach_earth_temple_many_mirrors_room(state, player)
        and state.has("Power Bracelets", player)
        and can_play_command_melody(state, player)
        and can_aim_mirror_shield(state, player),
    )
    set_rule_if_exists(
        "Earth Temple - Stalfos Crypt Room Chest",
        lambda state: can_reach_earth_temple_many_mirrors_room(state, player) and can_defeat_stalfos(state, player),
    )
    set_rule_if_exists(
        "Earth Temple - Big Key Chest",
        lambda state: can_reach_earth_temple_many_mirrors_room(state, player)
        and state.has("Power Bracelets", player)
        and can_play_command_melody(state, player)
        and can_aim_mirror_shield(state, player)
        and (
            can_defeat_blue_bubbles(state, player)
            or (has_heros_bow(state, player) and state._tww_obscure_1(player))
            or (
                (
                    has_heros_sword(state, player)
                    or has_any_master_sword(state, player)
                    or state.has("Skull Hammer", player)
                )
                and state._tww_obscure_1(player)
                and state._tww_precise_1(player)
            )
        )
        and can_defeat_darknuts(state, player),
    )
    set_rule_if_exists("Earth Temple - Jalhalla Heart Container", lambda state: can_defeat_jalhalla(state, player))

    # Wind Temple
    set_rule_if_exists(
        "Wind Temple - Between Dirt Patches Chest", lambda state: can_play_command_melody(state, player)
    )
    set_rule_if_exists(
        "Wind Temple - Behind Stone Head in Hidden Upper Room",
        lambda state: can_play_command_melody(state, player)
        and state.has_all(["Iron Boots", "Hookshot"], player)
        and can_fly_with_deku_leaf_indoors(state, player),
    )
    set_rule_if_exists(
        "Wind Temple - Tingle Statue Chest",
        lambda state: can_reach_wind_temple_kidnapping_room(state, player) and has_tingle_bombs(state, player),
    )
    set_rule_if_exists(
        "Wind Temple - Behind Stone Head Chest",
        lambda state: can_reach_wind_temple_kidnapping_room(state, player)
        and state.has_all(["Iron Boots", "Hookshot"], player),
    )
    set_rule_if_exists(
        "Wind Temple - Left Alcove Chest",
        lambda state: can_reach_wind_temple_kidnapping_room(state, player)
        and state.has("Iron Boots", player)
        and can_fan_with_deku_leaf(state, player),
    )
    set_rule_if_exists(
        "Wind Temple - Big Key Chest",
        lambda state: can_reach_wind_temple_kidnapping_room(state, player)
        and state.has("Iron Boots", player)
        and can_fan_with_deku_leaf(state, player)
        and can_play_wind_gods_aria(state, player)
        and can_defeat_darknuts(state, player),
    )
    set_rule_if_exists(
        "Wind Temple - Cyclones Room Chest",
        lambda state: can_reach_wind_temple_kidnapping_room(state, player)
        and (
            (
                state.has("Iron Boots", player)
                and can_fan_with_deku_leaf(state, player)
                and can_fly_with_deku_leaf_indoors(state, player)
                and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player))
            )
            or (
                state.has("Hookshot", player)
                and can_defeat_blue_bubbles(state, player)
                and can_fly_with_deku_leaf_indoors(state, player)
            )
            or (
                state.has("Hookshot", player)
                and can_fly_with_deku_leaf_indoors(state, player)
                and state._tww_obscure_1(player)
                and state._tww_precise_2(player)
            )
        ),
    )
    set_rule_if_exists(
        "Wind Temple - Behind Stone Head in Many Cyclones Room",
        lambda state: can_reach_end_of_wind_temple_many_cyclones_room(state, player) and state.has("Hookshot", player),
    )
    set_rule_if_exists(
        "Wind Temple - Hub Room Center Chest", lambda state: can_open_wind_temple_upper_giant_grate(state, player)
    )
    set_rule_if_exists(
        "Wind Temple - Spike Wall Room First Chest",
        lambda state: can_open_wind_temple_upper_giant_grate(state, player) and state.has("Iron Boots", player),
    )
    set_rule_if_exists(
        "Wind Temple - Spike Wall Room Destroy Floors",
        lambda state: can_open_wind_temple_upper_giant_grate(state, player) and state.has("Iron Boots", player),
    )
    set_rule_if_exists(
        "Wind Temple - Wizzrobe Mini Boss",
        lambda state: can_defeat_darknuts(state, player) and can_remove_peahat_armor(state, player),
    )
    set_rule_if_exists(
        "Wind Temple - Hub Room Top Chest", lambda state: can_activate_wind_temple_giant_fan(state, player)
    )
    set_rule_if_exists(
        "Wind Temple - Behind Armos Chest",
        lambda state: can_activate_wind_temple_giant_fan(state, player) and can_defeat_armos(state, player),
    )
    set_rule_if_exists(
        "Wind Temple - Kill All Basement Room Enemies",
        lambda state: can_reach_wind_temple_tall_basement_room(state, player)
        and can_defeat_stalfos(state, player)
        and can_defeat_wizzrobes(state, player)
        and can_defeat_morths(state, player),
    )
    set_rule_if_exists("Wind Temple - Molgera Heart Container", lambda state: can_defeat_molgera(state, player))

    # Ganon's Tower
    set_rule_if_exists(
        "Ganon's Tower - Maze Chest",
        lambda state: can_reach_ganons_tower_phantom_ganon_room(state, player)
        and can_defeat_phantom_ganon(state, player),
    )

    # Mailbox
    set_rule_if_exists(
        "Mailbox - Letter from Hoskit's Girlfriend",
        lambda state: state.has("Spoils Bag", player)
        and can_farm_golden_feathers(state, player)
        and can_play_song_of_passing(state, player),
    )
    set_rule_if_exists(
        "Mailbox - Letter from Baito's Mother",
        lambda state: state.has_all(["Delivery Bag", "Note to Mom"], player)
        and can_play_song_of_passing(state, player),
    )
    set_rule_if_exists(
        "Mailbox - Letter from Baito",
        lambda state: state.has_all(["Delivery Bag", "Note to Mom"], player)
        and state.can_reach_region("Jalhalla Boss Arena", player)
        and can_defeat_jalhalla(state, player),
    )
    set_rule_if_exists("Mailbox - Letter from Komali's Father", lambda state: state.has("Farore's Pearl", player))
    set_rule_if_exists("Mailbox - Letter Advertising Bombs in Beedle's Shop", lambda state: state.has("Bombs", player))
    set_rule_if_exists(
        "Mailbox - Letter Advertising Rock Spire Shop Ship", lambda state: has_any_wallet_upgrade(state, player)
    )
    # set_rule_if_exists(
    #     "Mailbox - Beedle's Silver Membership Reward",
    #     lambda state: (state.has_any(["Bait Bag", "Bombs", "Empty Bottle"], player) or has_heros_bow(state, player))
    #     and can_play_song_of_passing(state, player),
    # )
    # set_rule_if_exists(
    #     "Mailbox - Beedle's Gold Membership Reward",
    #     lambda state: (state.has_any(["Bait Bag", "Bombs", "Empty Bottle"], player) or has_heros_bow(state, player))
    #     and can_play_song_of_passing(state, player),
    # )
    set_rule_if_exists(
        "Mailbox - Letter from Orca",
        lambda state: state.can_reach_region("Kalle Demos Boss Arena", player)
        and can_defeat_kalle_demos(state, player),
    )
    set_rule_if_exists(
        "Mailbox - Letter from Grandma",
        lambda state: state.has("Empty Bottle", player) and can_play_song_of_passing(state, player),
    )
    set_rule_if_exists(
        "Mailbox - Letter from Aryll",
        lambda state: state.can_reach_region("Helmaroc King Boss Arena", player)
        and can_defeat_helmaroc_king(state, player)
        and can_play_song_of_passing(state, player),
    )
    set_rule_if_exists(
        "Mailbox - Letter from Tingle",
        lambda state: has_any_wallet_upgrade(state, player)
        and state.can_reach_region("Helmaroc King Boss Arena", player)
        and can_defeat_helmaroc_king(state, player)
        and can_play_song_of_passing(state, player),
    )

    # The Great Sea
    set_rule_if_exists("Great Sea - Beedle Shop 20 Rupee Item", lambda state: True)
    set_rule_if_exists("Great Sea - Salvage Corp Gift", lambda state: True)
    set_rule_if_exists("Great Sea - Cyclos", lambda state: has_heros_bow(state, player))
    set_rule_if_exists("Great Sea - Goron Trading Reward", lambda state: state.has("Delivery Bag", player))
    set_rule_if_exists(
        "Great Sea - Withered Trees",
        lambda state: can_access_forest_haven(state, player)
        and state.has("Empty Bottle", player)
        and can_play_ballad_of_gales(state, player)
        and state.can_reach_region("Cliff Plateau Isles Inner Cave", player),
    )
    set_rule_if_exists(
        "Great Sea - Ghost Ship Chest",
        lambda state: state.has("Ghost Ship Chart", player)
        and can_play_ballad_of_gales(state, player)
        and can_defeat_wizzrobes(state, player)
        and can_defeat_redeads(state, player)
        and can_defeat_stalfos(state, player),
    )

    # Private Oasis
    set_rule_if_exists(
        "Private Oasis - Top of Waterfall Chest",
        lambda state: state.has("Hookshot", player) or can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists(
        "Private Oasis - Cabana Labyrinth Lower Floor Chest", lambda state: state.has("Skull Hammer", player)
    )
    set_rule_if_exists(
        "Private Oasis - Cabana Labyrinth Upper Floor Chest",
        lambda state: state.has("Skull Hammer", player) and can_play_winds_requiem(state, player),
    )
    set_rule_if_exists(
        "Private Oasis - Big Octo",
        lambda state: can_defeat_big_octos(state, player) and state.has("Grappling Hook", player),
    )

    # Spectacle Island
    set_rule_if_exists("Spectacle Island - Barrel Shooting First Prize", lambda state: True)
    set_rule_if_exists("Spectacle Island - Barrel Shooting Second Prize", lambda state: True)

    # Needle Rock Isle
    set_rule_if_exists("Needle Rock Isle - Chest", lambda state: state.has("Bait Bag", player))
    set_rule_if_exists("Needle Rock Isle - Cave Chest", lambda state: has_fire_arrows(state, player))
    set_rule_if_exists(
        "Needle Rock Isle - Golden Gunboat", lambda state: state.has_all(["Bombs", "Grappling Hook"], player)
    )

    # Angular Isles
    set_rule_if_exists("Angular Isles - Peak Chest", lambda state: True)
    set_rule_if_exists(
        "Angular Isles - Cave Chest",
        lambda state: can_aim_mirror_shield(state, player)
        and (can_fly_with_deku_leaf_indoors(state, player) or state.has("Hookshot", player)),
    )

    # Boating Course
    set_rule_if_exists("Boating Course - Raft Chest", lambda state: True)
    set_rule_if_exists(
        "Boating Course - Cave Chest",
        lambda state: can_hit_diamond_switches_at_range(state, player)
        and (can_defeat_miniblins_easily(state, player) or state._tww_precise_2(player)),
    )

    # Stone Watcher Island
    set_rule_if_exists(
        "Stone Watcher Island - Cave Chest",
        lambda state: can_defeat_armos(state, player)
        and can_defeat_wizzrobes(state, player)
        and can_defeat_darknuts(state, player)
        and can_play_winds_requiem(state, player),
    )
    set_rule_if_exists("Stone Watcher Island - Lookout Platform Chest", lambda state: True)
    set_rule_if_exists(
        "Stone Watcher Island - Lookout Platform Destroy Cannons",
        lambda state: can_destroy_cannons(state, player),
    )

    # Islet of Steel
    set_rule_if_exists(
        "Islet of Steel - Interior Chest", lambda state: state.has("Bombs", player) and can_play_winds_requiem(state, player)
    )
    set_rule_if_exists(
        "Islet of Steel - Lookout Platform Defeat Enemies",
        lambda state: can_defeat_wizzrobes_at_range(state, player),
    )

    # Overlook Island
    set_rule_if_exists(
        "Overlook Island - Cave Chest",
        lambda state: can_defeat_stalfos(state, player)
        and can_defeat_wizzrobes(state, player)
        and can_defeat_red_chuchus(state, player)
        and can_defeat_green_chuchus(state, player)
        and can_defeat_keese(state, player)
        and can_defeat_fire_keese(state, player)
        and can_defeat_morths(state, player)
        and can_defeat_kargarocs(state, player)
        and can_defeat_darknuts(state, player)
        and can_play_winds_requiem(state, player),
    )

    # Bird's Peak Rock
    set_rule_if_exists("Birds Peak Rock - Cave Chest", lambda state: can_play_winds_requiem(state, player))

    # Pawprint Isle
    set_rule_if_exists("Pawprint Isle - Chu Chu Cave Chest", lambda state: True)
    set_rule_if_exists(
        "Pawprint Isle - Chu Chu Cave Chest Behind Left Boulder", lambda state: can_move_boulders(state, player)
    )
    set_rule_if_exists(
        "Pawprint Isle - Chu Chu Cave Chest Behind Right Boulder", lambda state: can_move_boulders(state, player)
    )
    set_rule_if_exists(
        "Pawprint Isle - Chu Chu Cave Chest Scale Wall", lambda state: state.has("Grappling Hook", player)
    )
    set_rule_if_exists(
        "Pawprint Isle - Wizzrobe Cave Chest",
        lambda state: can_defeat_wizzrobes_at_range(state, player)
        and can_defeat_fire_keese(state, player)
        and can_defeat_magtails(state, player)
        and can_defeat_red_chuchus(state, player)
        and can_defeat_green_chuchus(state, player)
        and can_defeat_yellow_chuchus(state, player)
        and can_defeat_red_bubbles(state, player)
        and can_remove_peahat_armor(state, player),
    )
    set_rule_if_exists("Pawprint Isle - Lookout Platform Defeat Enemies", lambda state: True)

    # Thorned Fairy Island
    set_rule_if_exists("Thorned Fairy Island - Great Fairy", lambda state: True)
    set_rule_if_exists(
        "Thorned Fairy Island - Northeastern Lookout Platform Destroy Cannons",
        lambda state: can_destroy_cannons(state, player),
    )
    set_rule_if_exists(
        "Thorned Fairy Island - Southwestern Lookout Platform Defeat Enemies",
        lambda state: can_fly_with_deku_leaf_outdoors(state, player),
    )

    # Eastern Fairy Island
    set_rule_if_exists("Eastern Fairy Island - Great Fairy", lambda state: True)
    set_rule_if_exists(
        "Eastern Fairy Island - Lookout Platform Defeat Cannons and Enemies",
        lambda state: can_destroy_cannons(state, player),
    )

    # Western Fairy Island
    set_rule_if_exists("Western Fairy Island - Great Fairy", lambda state: True)
    set_rule_if_exists("Western Fairy Island - Lookout Platform Chest", lambda state: True)

    # Southern Fairy Island
    set_rule_if_exists("Southern Fairy Island - Great Fairy", lambda state: True)
    set_rule_if_exists(
        "Southern Fairy Island - Lookout Platform Destroy Northwest Cannons",
        lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists(
        "Southern Fairy Island - Lookout Platform Destroy Southeast Cannons",
        lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
    )

    # Northern Fairy Island
    set_rule_if_exists("Northern Fairy Island - Great Fairy", lambda state: True)
    set_rule_if_exists("Northern Fairy Island - Submarine Chest", lambda state: True)

    # Tingle Island
    set_rule_if_exists(
        "Tingle Island - Ankle All Statues Reward",
        lambda state: state.has_group_unique("Tingle Statues", player, 5),
    )
    set_rule_if_exists(
        "Tingle Island - Big Octo",
        lambda state: can_defeat_12_eye_big_octos(state, player) and state.has("Grappling Hook", player),
    )

    # Diamond Steppe Island
    set_rule_if_exists("Diamond Steppe Island - Maze First Chest", lambda state: True)
    set_rule_if_exists("Diamond Steppe Island - Maze Second Chest", lambda state: True)
    set_rule_if_exists(
        "Diamond Steppe Island - Big Octo",
        lambda state: can_defeat_big_octos(state, player) and state.has("Grappling Hook", player),
    )

    # Bomb Island
    set_rule_if_exists("Bomb Island - Cave Chest", lambda state: can_stun_magtails(state, player))
    set_rule_if_exists("Bomb Island - Lookout Platform Defeat Enemies", lambda state: True)
    set_rule_if_exists("Bomb Island - Submarine Chest", lambda state: True)

    # Rock Spire Isle
    set_rule_if_exists("Rock Spire Isle - Cave Chest", lambda state: True)
    set_rule_if_exists(
        "Rock Spire Isle - Beedle 500 Rupee Item",
        lambda state: has_any_wallet_upgrade(state, player),
    )
    set_rule_if_exists(
        "Rock Spire Isle - Beedle 950 Rupee Item",
        lambda state: has_any_wallet_upgrade(state, player),
    )
    set_rule_if_exists(
        "Rock Spire Isle - Beedle 900 Rupee Item",
        lambda state: has_any_wallet_upgrade(state, player),
    )
    set_rule_if_exists(
        "Rock Spire Isle - Western Lookout Platform Destroy Cannons",
        lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists(
        "Rock Spire Isle - Eastern Lookout Platform Destroy Cannons",
        lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists("Rock Spire Isle - Center Lookout Platform Chest", lambda state: True)
    set_rule_if_exists(
        "Rock Spire Isle - Defeat Southeast Gunboat", lambda state: state.has_all(["Bombs", "Grappling Hook"], player)
    )

    # Shark Island
    set_rule_if_exists("Shark Island - Cave Chest", lambda state: can_defeat_miniblins(state, player))

    # Cliff Plateau Isles
    set_rule_if_exists(
        "Cliff Plateau Isles - Cave Chest",
        lambda state: can_defeat_boko_babas(state, player)
        or (state.has("Grappling Hook", player) and state._tww_obscure_1(player) and state._tww_precise_1(player)),
    )
    set_rule_if_exists("Cliff Plateau Isles - Highest Isle Chest", lambda state: True)
    set_rule_if_exists("Cliff Plateau Isles - Lookout Platform Chest", lambda state: True)

    # Crescent Moon Island
    set_rule_if_exists("Crescent Moon Island - Chest on Island", lambda state: True)
    set_rule_if_exists("Crescent Moon Island - Submarine Chest", lambda state: can_defeat_miniblins(state, player))

    # Horseshoe Island
    set_rule_if_exists(
        "Horseshoe Island - Play Golf",
        lambda state: can_fan_with_deku_leaf(state, player)
        and (can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)),
    )
    set_rule_if_exists(
        "Horseshoe Island - Cave Chest",
        lambda state: can_defeat_mothulas(state, player) and can_defeat_winged_mothulas(state, player),
    )
    set_rule_if_exists("Horseshoe Island - Northwestern Lookout Platform Chest", lambda state: True)
    set_rule_if_exists("Horseshoe Island - Southeastern Lookout Platform Chest", lambda state: True)

    # Flight Control Platform
    set_rule_if_exists(
        "Flight Control Platform - First Prize",
        lambda state: can_fly_with_deku_leaf_outdoors(state, player) and has_magic_meter_upgrade(state, player),
    )
    set_rule_if_exists(
        "Flight Control Platform - Submarine Chest",
        lambda state: can_defeat_wizzrobes(state, player)
        and can_defeat_red_chuchus(state, player)
        and can_defeat_green_chuchus(state, player)
        and can_defeat_miniblins(state, player)
        and can_defeat_wizzrobes_at_range(state, player),
    )

    # Star Island
    set_rule_if_exists("Star Island - Cave Chest", lambda state: can_defeat_magtails(state, player))
    set_rule_if_exists("Star Island - Lookout Platform Chest", lambda state: True)

    # Star Belt Archipelago
    set_rule_if_exists("Star Belt Archipelago - Lookout Platform Chest", lambda state: True)

    # Five-Star Isles
    set_rule_if_exists(
        "Five Star Isles - Lookout Platform Destroy Cannons", lambda state: can_destroy_cannons(state, player)
    )
    set_rule_if_exists("Five Star Isles - Raft Chest", lambda state: True)
    set_rule_if_exists("Five Star Isles - Submarine Chest", lambda state: True)

    # Seven-Star Isles
    set_rule_if_exists("Seven Star Isles - Center Lookout Platform Chest", lambda state: True)
    set_rule_if_exists("Seven Star Isles - Northern Lookout Platform Chest", lambda state: True)
    set_rule_if_exists(
        "Seven Star Isles - Southern Lookout Platform Chest", lambda state: can_defeat_wizzrobes_at_range(state, player)
    )
    set_rule_if_exists(
        "Seven Star Isles - Big Octo",
        lambda state: can_defeat_12_eye_big_octos(state, player) and state.has("Grappling Hook", player),
    )

    # Cyclops Reef
    set_rule_if_exists(
        "Cyclops Reef - Destroy Cannons and Gunboats",
        lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists("Cyclops Reef - Lookout Platform Defeat Enemies", lambda state: True)

    # Two-Eye Reef
    set_rule_if_exists(
        "Two Eye Reef - Destroy Cannons and Gunboats",
        lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists("Two Eye Reef - Lookout Platform Chest", lambda state: True)
    set_rule_if_exists("Two Eye Reef - Big Octo Great Fairy", lambda state: can_defeat_big_octos(state, player))

    # Three-Eye Reef
    set_rule_if_exists(
        "Three Eye Reef - Destroy Cannons and Gunboats",
        lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
    )

    # Four-Eye Reef
    set_rule_if_exists(
        "Four Eye Reef - Destroy Cannons and Gunboats",
        lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
    )

    # Five-Eye Reef
    set_rule_if_exists(
        "Five Eye Reef - Destroy Cannons",
        lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists("Five Eye Reef - Lookout Platform Chest", lambda state: True)

    # Six-Eye Reef
    set_rule_if_exists(
        "Six Eye Reef - Destroy Cannons and Gunboats",
        lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
    )
    set_rule_if_exists(
        "Six Eye Reef - Lookout Platform Destroy Cannons", lambda state: can_destroy_cannons(state, player)
    )
    set_rule_if_exists("Six Eye Reef - Submarine Chest", lambda state: True)

    # Sunken Treasure
    set_rule_if_exists(
        "Forsaken Fortress Sector - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 1),
    )
    set_rule_if_exists(
        "Star Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 2),
    )
    set_rule_if_exists(
        "Northern Fairy Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 3),
    )
    set_rule_if_exists(
        "Gale Isle - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 4),
    )
    set_rule_if_exists(
        "Crescent Moon Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 5),
    )
    set_rule_if_exists(
        "Seven Star Isles - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 6)
        and (state.has("Bombs", player) or state._tww_precise_1(player)),
    )
    set_rule_if_exists(
        "Overlook Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 7),
    )
    set_rule_if_exists(
        "Four Eye Reef - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 8)
        and (
            state.has("Bombs", player)
            or state._tww_precise_1(player)
            or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
        ),
    )
    set_rule_if_exists(
        "Mother & Child Isles - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 9),
    )
    set_rule_if_exists(
        "Spectacle Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 10),
    )
    set_rule_if_exists(
        "Windfall Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 11),
    )
    set_rule_if_exists(
        "Pawprint Isle - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 12),
    )
    set_rule_if_exists(
        "Dragon Roost Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 13),
    )
    set_rule_if_exists(
        "Flight Control Platform - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 14),
    )
    set_rule_if_exists(
        "Western Fairy Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 15),
    )
    set_rule_if_exists(
        "Rock Spire Isle - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 16),
    )
    set_rule_if_exists(
        "Tingle Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 17),
    )
    set_rule_if_exists(
        "Northern Triangle Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 18),
    )
    set_rule_if_exists(
        "Eastern Fairy Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 19),
    )
    set_rule_if_exists(
        "Fire Mountain - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 20),
    )
    set_rule_if_exists(
        "Star Belt Archipelago - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 21),
    )
    set_rule_if_exists(
        "Three Eye Reef - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 22)
        and (
            state.has("Bombs", player)
            or state._tww_precise_1(player)
            or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
        ),
    )
    set_rule_if_exists(
        "Greatfish Isle - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 23),
    )
    set_rule_if_exists(
        "Cyclops Reef - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 24)
        and (
            state.has("Bombs", player)
            or state._tww_precise_1(player)
            or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
        ),
    )
    set_rule_if_exists(
        "Six Eye Reef - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 25)
        and (
            state.has("Bombs", player)
            or state._tww_precise_1(player)
            or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
        ),
    )
    set_rule_if_exists(
        "Tower of the Gods Sector - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 26),
    )
    set_rule_if_exists(
        "Eastern Triangle Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 27),
    )
    set_rule_if_exists(
        "Thorned Fairy Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 28),
    )
    set_rule_if_exists(
        "Needle Rock Isle - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 29),
    )
    set_rule_if_exists(
        "Islet of Steel - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 30),
    )
    set_rule_if_exists(
        "Stone Watcher Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 31),
    )
    set_rule_if_exists(
        "Southern Triangle Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 32)
        and (can_defeat_seahats(state, player) or state._tww_precise_1(player)),
    )
    set_rule_if_exists(
        "Private Oasis - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 33),
    )
    set_rule_if_exists(
        "Bomb Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 34),
    )
    set_rule_if_exists(
        "Birds Peak Rock - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 35),
    )
    set_rule_if_exists(
        "Diamond Steppe Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 36),
    )
    set_rule_if_exists(
        "Five Eye Reef - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 37)
        and can_destroy_cannons(state, player),
    )
    set_rule_if_exists(
        "Shark Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 38),
    )
    set_rule_if_exists(
        "Southern Fairy Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 39),
    )
    set_rule_if_exists(
        "Ice Ring Isle - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 40),
    )
    set_rule_if_exists(
        "Forest Haven - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 41),
    )
    set_rule_if_exists(
        "Cliff Plateau Isles - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 42),
    )
    set_rule_if_exists(
        "Horseshoe Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 43),
    )
    set_rule_if_exists(
        "Outset Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 44),
    )
    set_rule_if_exists(
        "Headstone Island - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 45),
    )
    set_rule_if_exists(
        "Two Eye Reef - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player)
        and state._tww_has_chart_for_island(player, 46)
        and (
            state.has("Bombs", player)
            or state._tww_precise_1(player)
            or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
        ),
    )
    set_rule_if_exists(
        "Angular Isles - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 47),
    )
    set_rule_if_exists(
        "Boating Course - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 48),
    )
    set_rule_if_exists(
        "Five Star Isles - Sunken Treasure",
        lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 49),
    )

    set_rule_if_exists("Defeat Ganondorf", lambda state: can_reach_and_defeat_ganondorf(state, player))

    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

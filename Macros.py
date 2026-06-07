from BaseClasses import CollectionState


def can_play_winds_requiem(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Wind's Requiem"], player)


def can_play_ballad_of_gales(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Ballad of Gales"], player)


def can_play_command_melody(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Command Melody"], player)


def can_play_earth_gods_lyric(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Earth God's Lyric"], player)


def can_play_wind_gods_aria(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Wind God's Aria"], player)


def can_play_song_of_passing(state: CollectionState, player: int) -> bool:
    return state.has_all(["Wind Waker", "Song of Passing"], player)


def can_fan_with_deku_leaf(state: CollectionState, player: int) -> bool:
    return state.has("Deku Leaf", player)


def can_fly_with_deku_leaf_indoors(state: CollectionState, player: int) -> bool:
    return state.has("Deku Leaf", player) and has_magic_meter(state, player)


def can_fly_with_deku_leaf_outdoors(state: CollectionState, player: int) -> bool:
    return state.has("Deku Leaf", player) and has_magic_meter(state, player) and can_play_winds_requiem(state, player)


def can_use_magic_armor(state: CollectionState, player: int) -> bool:
    return state.has("Magic Armor", player) and has_magic_meter(state, player)


def can_aim_mirror_shield(state: CollectionState, player: int) -> bool:
    return has_mirror_shield(state, player) and (
        state.has_any(["Wind Waker", "Grappling Hook", "Boomerang", "Deku Leaf", "Hookshot"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_move_boulders(state: CollectionState, player: int) -> bool:
    return state.has_any(["Bombs", "Power Bracelets"], player)


def can_defeat_door_flowers(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Bombs", "Hookshot"], player) or has_heros_bow(state, player)


def can_hit_diamond_switches_at_range(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Hookshot"], player) or has_heros_bow(state, player)


def can_destroy_seeds_hanging_by_vines(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Bombs", "Hookshot"], player) or has_heros_bow(state, player)


def has_heros_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 1)


def has_any_master_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 2)


def has_full_power_master_sword(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Sword", player, 4)


def has_heros_shield(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Shield", player, 1)


def has_mirror_shield(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Shield", player, 2)


def has_heros_bow(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 1)


def has_fire_arrows(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 2) and has_magic_meter(state, player)


def has_ice_arrows(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 2) and has_magic_meter(state, player)


def has_light_arrows(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Bow", player, 3) and has_magic_meter(state, player)


def has_any_wallet_upgrade(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Wallet", player, 1)


def has_picto_box(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Picto Box", player, 1)


def has_deluxe_picto_box(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Picto Box", player, 2)


def has_any_quiver_upgrade(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Quiver", player, 1)


def has_magic_meter(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Magic Meter", player, 1)


def has_magic_meter_upgrade(state: CollectionState, player: int) -> bool:
    return state.has("Progressive Magic Meter", player, 2)


def has_all_8_triforce_shards(state: CollectionState, player: int) -> bool:
    return state.has_group_unique("Shards", player, 8)

def has_tingle_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player)

def can_reach_outset_island_upper_level(state: CollectionState, player: int) -> bool:
    return can_cut_down_outset_trees(state, player) or (
        can_fly_with_deku_leaf_outdoors(state, player) and state._twwhd_obscure_1(player)
    )


def can_access_forest_of_fairies(state: CollectionState, player: int) -> bool:
    return can_reach_outset_island_upper_level(state, player) and can_fly_with_deku_leaf_outdoors(state, player)


def can_reach_dragon_roost_cavern_gaping_maw(state: CollectionState, player: int) -> bool:
    return state.has("Dragon Roost Cavern Small Key", player, 1) and (
        (state.has("Dragon Roost Cavern Small Key", player, 4) and can_cut_down_hanging_drc_platform(state, player))
        or (can_fly_with_deku_leaf_indoors(state, player) and state._twwhd_obscure_2(player))
        or (has_ice_arrows(state, player) and state._twwhd_obscure_2(player) and state._twwhd_precise_1(player))
    )


def can_reach_dragon_roost_cavern_boss_stairs(state: CollectionState, player: int) -> bool:
    return state.has("Dragon Roost Cavern Small Key", player, 4) and (
        state.has_any(["Grappling Hook", "Hookshot"], player)
        or can_fly_with_deku_leaf_indoors(state, player)
        or has_ice_arrows(state, player)
    )


def can_reach_tower_of_the_gods_second_floor(state: CollectionState, player: int) -> bool:
    return state.has_all(["Bombs", "Tower of the Gods Small Key"], player) and can_defeat_yellow_chuchus(state, player)


def can_reach_tower_of_the_gods_third_floor(state: CollectionState, player: int) -> bool:
    return (
        can_reach_tower_of_the_gods_second_floor(state, player)
        and can_bring_west_servant_of_the_tower(state, player)
        and can_bring_north_servant_of_the_tower(state, player)
        and state.has("Wind Waker", player)
    )


def can_bring_west_servant_of_the_tower(state: CollectionState, player: int) -> bool:
    return (
        (state.has("Grappling Hook", player) or can_fly_with_deku_leaf_indoors(state, player))
        and can_play_command_melody(state, player)
        and has_heros_bow(state, player)
    )


def can_bring_north_servant_of_the_tower(state: CollectionState, player: int) -> bool:
    return (
        state.has("Tower of the Gods Small Key", player, 2)
        and (can_fly_with_deku_leaf_indoors(state, player) or state._twwhd_obscure_1(player))
        and can_play_command_melody(state, player)
    )


def can_reach_earth_temple_sun_statue_room(state: CollectionState, player: int) -> bool:
    return (
        can_play_command_melody(state, player)
        and can_defeat_red_chuchus(state, player)
        and can_defeat_green_chuchus(state, player)
    )


def can_reach_earth_temple_right_path(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_sun_statue_room(state, player)
        and can_play_command_melody(state, player)
        and state.has("Skull Hammer", player)
    )


def can_reach_earth_temple_left_path(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_sun_statue_room(state, player) and state.has("Earth Temple Small Key", player, 2)


def can_reach_earth_temple_moblins_and_poes_room(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_left_path(state, player)
        and has_fire_arrows(state, player)
        and state.has("Power Bracelets", player)
        and can_defeat_floormasters(state, player)
        and (can_play_command_melody(state, player) or has_mirror_shield(state, player))
    )


def can_reach_earth_temple_basement(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_sun_statue_room(state, player)
        and can_play_command_melody(state, player)
        and can_aim_mirror_shield(state, player)
    )


def can_reach_earth_temple_redead_hub_room(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_basement(state, player) and can_play_earth_gods_lyric(state, player)


def can_reach_earth_temple_third_crypt(state: CollectionState, player: int) -> bool:
    return (
        can_reach_earth_temple_redead_hub_room(state, player)
        and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player))
        and state.has_all_counts({"Power Bracelets": 1, "Skull Hammer": 1, "Earth Temple Small Key": 3}, player)
        and (can_defeat_red_bubbles(state, player) or state._twwhd_precise_2(player))
        and can_play_command_melody(state, player)
        and can_aim_mirror_shield(state, player)
    )


def can_reach_earth_temple_tall_vine_room(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_third_crypt(state, player) and can_play_earth_gods_lyric(state, player)


def can_reach_earth_temple_many_mirrors_room(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_tall_vine_room(state, player)


def can_reach_wind_temple_kidnapping_room(state: CollectionState, player: int) -> bool:
    return (
        can_play_command_melody(state, player)
        and state.has("Iron Boots", player)
        and can_fly_with_deku_leaf_indoors(state, player)
    )


def can_reach_end_of_wind_temple_many_cyclones_room(state: CollectionState, player: int) -> bool:
    return can_reach_wind_temple_kidnapping_room(state, player) and (
        (
            state.has("Iron Boots", player)
            and can_fan_with_deku_leaf(state, player)
            and can_fly_with_deku_leaf_indoors(state, player)
            and can_cut_grass(state, player)
        )
        or (
            state.has("Hookshot", player)
            and can_defeat_blue_bubbles(state, player)
            and can_fly_with_deku_leaf_indoors(state, player)
        )
        or (
            state.has("Hookshot", player)
            and can_fly_with_deku_leaf_indoors(state, player)
            and state._twwhd_obscure_1(player)
            and state._twwhd_precise_2(player)
        )
    )


def can_open_wind_temple_upper_giant_grate(state: CollectionState, player: int) -> bool:
    return can_reach_end_of_wind_temple_many_cyclones_room(state, player) and state.has("Iron Boots", player)


def can_activate_wind_temple_giant_fan(state: CollectionState, player: int) -> bool:
    return can_open_wind_temple_upper_giant_grate(state, player) and can_play_command_melody(state, player)


def can_open_wind_temple_lower_giant_grate(state: CollectionState, player: int) -> bool:
    return (
        can_reach_wind_temple_kidnapping_room(state, player)
        and state.has("Hookshot", player)
        and can_defeat_blue_bubbles(state, player)
    )


def can_reach_wind_temple_tall_basement_room(state: CollectionState, player: int) -> bool:
    return (
        can_open_wind_temple_upper_giant_grate(state, player)
        and can_open_wind_temple_lower_giant_grate(state, player)
        and state.has("Wind Temple Small Key", player, 2)
    )


def can_access_dragon_roost_pond_past_statues_to_drc_first_room(state: CollectionState, player: int) -> bool:
    return True


def can_access_forest_haven(state: CollectionState, player: int) -> bool:
    return state.has("Grappling Hook", player) or can_fly_with_deku_leaf_outdoors(state, player)


def can_access_fw_entrance_platform_to_fw_first_room(state: CollectionState, player: int) -> bool:
    return (
        can_access_forest_haven(state, player)
        and (
            state.has("Grappling Hook", player)
            or (
                can_fly_with_deku_leaf_indoors(state, player)
                and can_fly_with_deku_leaf_outdoors(state, player)
                and state._twwhd_obscure_1(player)
                and state._twwhd_precise_1(player)
            )
        )
        and can_fly_with_deku_leaf_outdoors(state, player)
        and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player))
    )


def can_access_tower_of_the_gods_sector_to_totg_entrance_room(state: CollectionState, player: int) -> bool:
    return state.has_group_unique("Pearls", player, 3)


def can_access_dungeon_entrance_in_forsaken_fortress_sector(state: CollectionState, player: int) -> bool:
    return False


def can_access_headstone_island_interior_to_et_first_room(state: CollectionState, player: int) -> bool:
    return state.has("Power Bracelets", player)


def can_access_gale_isle_interior_to_wt_first_room(state: CollectionState, player: int) -> bool:
    return state.has_all(["Iron Boots", "Skull Hammer"], player)


def can_access_fw_tall_room_before_mini_boss_to_fw_mini_boss_room(state: CollectionState, player: int) -> bool:
    return (
        can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and state.has_all(["Grappling Hook", "Forbidden Woods Small Key"], player)
    )


def can_access_totg_west_servant_corridor_near_mini_boss_room_to_totg_mini_boss_room(state: CollectionState, player: int) -> bool:
    return (
        can_reach_tower_of_the_gods_second_floor(state, player)
        and (state.has("Grappling Hook", player) or can_fly_with_deku_leaf_indoors(state, player))
        and (can_play_command_melody(state, player) or has_heros_bow(state, player))
    )


def can_access_et_two_moblins_and_poes_room_past_stairs_to_et_mini_boss_room(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_moblins_and_poes_room(state, player) and state.has("Earth Temple Small Key", player, 3)


def can_access_wt_hub_room_basement_above_fan_to_wt_mini_boss_room(state: CollectionState, player: int) -> bool:
    return can_open_wind_temple_upper_giant_grate(state, player) and state.has("Wind Temple Small Key", player, 2)


def can_access_hyrule_castle_interior_to_hyrule_castle_sword_chamber(state: CollectionState, player: int) -> bool:
    return can_access_hyrule(state, player)


def can_access_drc_boss_door_room_across_lava_to_gohma_battle_arena(state: CollectionState, player: int) -> bool:
    return can_reach_dragon_roost_cavern_boss_stairs(state, player) and state.has("Dragon Roost Cavern Big Key", player)


def can_access_fw_boss_door_room_to_kalle_demos_battle_arena(state: CollectionState, player: int) -> bool:
    return (
        can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_boko_babas(state, player)
        and (can_defeat_door_flowers(state, player) or state.has("Grappling Hook", player))
        and can_defeat_mothulas(state, player)
        and state.has("Forbidden Woods Big Key", player)
    )


def can_access_totg_outside_area_to_gohdan_battle_arena(state: CollectionState, player: int) -> bool:
    return (
        can_reach_tower_of_the_gods_third_floor(state, player)
        and can_defeat_armos(state, player)
        and state.has("Tower of the Gods Big Key", player)
    )


def can_access_forsaken_fortress_before_boss_door_to_helmaroc_king_battle_arena(state: CollectionState, player: int) -> bool:
    return (
        can_get_inside_forsaken_fortress(state, player)
        and state.has("Skull Hammer", player)
        and (
            can_fly_with_deku_leaf_indoors(state, player)
            or state.has("Hookshot", player)
            or (state._twwhd_obscure_2(player) and state._twwhd_precise_2(player))
        )
        and (
            can_defeat_bokoblins(state, player)
            or can_fly_with_deku_leaf_outdoors(state, player)
            or state.has("Grappling Hook", player)
        )
    )


def can_access_et_boss_door_room_to_jalhalla_battle_arena(state: CollectionState, player: int) -> bool:
    return can_reach_earth_temple_tall_vine_room(state, player) and state.has("Earth Temple Big Key", player)


def can_access_wt_three_big_fans_room_past_song_stone_to_molgera_battle_arena(state: CollectionState, player: int) -> bool:
    return (
        can_reach_wind_temple_tall_basement_room(state, player)
        and state.has_all(["Hookshot", "Iron Boots", "Wind Temple Big Key"], player)
        and can_play_command_melody(state, player)
        and can_play_wind_gods_aria(state, player)
    )


def can_access_outset_near_savage_headstone_to_outset_savage_labyrinth(state: CollectionState, player: int) -> bool:
    return (
        (can_reach_outset_island_upper_level(state, player) and can_fly_with_deku_leaf_outdoors(state, player))
        or state.has("Hookshot", player)
    ) and state.has("Power Bracelets", player)


def can_access_dragon_roost_island_to_dragon_roost_island_cave(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_fire_mountain_to_fire_mountain_interior(state: CollectionState, player: int) -> bool:
    return has_ice_arrows(state, player)


def can_access_ice_ring_isle_to_ice_ring_interior(state: CollectionState, player: int) -> bool:
    return has_fire_arrows(state, player)


def can_access_the_cabana_to_cabana_labyrinth(state: CollectionState, player: int) -> bool:
    return state.has_all(["Delivery Bag", "Cabana Deed", "Grappling Hook"], player)


def can_access_needle_rock_isle_to_needle_rock_cave(state: CollectionState, player: int) -> bool:
    return has_fire_arrows(state, player)


def can_access_angular_isles_small_isle_to_angular_isles_cave(state: CollectionState, player: int) -> bool:
    return can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)


def can_access_boating_course_small_isle_to_boating_course_cave(state: CollectionState, player: int) -> bool:
    return can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)


def can_access_stone_watcher_island_to_stone_watcher_cave(state: CollectionState, player: int) -> bool:
    return state.has("Power Bracelets", player)


def can_access_overlook_island_upper_isles_to_overlook_cave(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player)


def can_access_birds_peak_rock_behind_bars_to_birds_peak_rock_cave(state: CollectionState, player: int) -> bool:
    return state.has("Bait Bag", player)


def can_access_pawprint_isle_to_pawprint_chu_chu_cave(state: CollectionState, player: int) -> bool:
    return True


def can_access_pawprint_wizzrobe_cave_isle_to_pawprint_wizzrobe_cave(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player)


def can_access_diamond_steppe_upper_island_to_diamond_steppe_warp_maze(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player)


def can_access_bomb_island_to_bomb_island_cave(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_rock_spire_upper_ledges_to_rock_spire_cave(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player)


def can_access_shark_island_to_shark_island_cave(state: CollectionState, player: int) -> bool:
    return state.has_all(["Iron Boots", "Skull Hammer"], player)


def can_access_cliff_plateau_isles_to_cliff_plateau_cave(state: CollectionState, player: int) -> bool:
    return True


def can_access_horseshoe_island_past_tentacles_to_horseshoe_cave(state: CollectionState, player: int) -> bool:
    return can_fan_with_deku_leaf(state, player)


def can_access_star_island_to_star_island_cave(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_ice_ring_interior_to_ice_ring_inner_cave(state: CollectionState, player: int) -> bool:
    return state.has("Iron Boots", player)


def can_access_cliff_plateau_highest_isle_to_cliff_plateau_cave_past_wooden_barrier(state: CollectionState, player: int) -> bool:
    return can_defeat_boko_babas(state, player) and can_fly_with_deku_leaf_indoors(state, player)


def can_access_outset_forest_of_fairies_to_outset_island_inside_great_fairy_fountain(state: CollectionState, player: int) -> bool:
    return can_access_forest_of_fairies(state, player) and can_move_boulders(state, player)


def can_access_thorned_fairy_island_past_tentacles_to_thorned_fairy_island_inside_great_fairy_fountain(state: CollectionState, player: int) -> bool:
    return state.has("Skull Hammer", player)


def can_access_eastern_fairy_island_past_boulder_to_eastern_fairy_island_inside_great_fairy_fountain(state: CollectionState, player: int) -> bool:
    return can_move_boulders(state, player)


def can_access_western_fairy_island_past_flames_to_western_fairy_island_inside_great_fairy_fountain(state: CollectionState, player: int) -> bool:
    return state.has("Skull Hammer", player)


def can_access_southern_fairy_island_behind_wooden_barrier_to_southern_fairy_island_inside_great_fairy_fountain(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player) or has_fire_arrows(state, player)


def can_access_northern_fairy_island_to_northern_fairy_island_inside_great_fairy_fountain(state: CollectionState, player: int) -> bool:
    return True


def can_get_past_forsaken_fortress_gate(state: CollectionState, player: int) -> bool:
    return (
        state.has("Bombs", player)
        or (state._twwhd_obscure_1(player) and state._twwhd_precise_1(player))
        or (can_open_ganons_tower_dark_portal(state, player) and state._twwhd_obscure_1(player))
    )


def can_get_inside_forsaken_fortress(state: CollectionState, player: int) -> bool:
    return can_get_past_forsaken_fortress_gate(state, player) and state.has("Skull Hammer", player)


def can_reach_and_defeat_phantom_ganon(state: CollectionState, player: int) -> bool:
    return can_get_past_forsaken_fortress_gate(state, player) and can_defeat_phantom_ganon(state, player)


def can_defeat_phantom_ganon(state: CollectionState, player: int) -> bool:
    return (state._twwhd_outside_swordless_mode(player) and has_any_master_sword(state, player)) or (
        state._twwhd_in_swordless_mode(player) and state.has("Skull Hammer", player)
    )


def can_access_hyrule(state: CollectionState, player: int) -> bool:
    return has_all_8_triforce_shards(state, player)


def can_get_past_hyrule_barrier(state: CollectionState, player: int) -> bool:
    return can_access_hyrule(state, player) and (
        has_full_power_master_sword(state, player) or state._twwhd_in_swordless_mode(player)
    )


def can_access_ganons_tower(state: CollectionState, player: int) -> bool:
    return can_get_past_hyrule_barrier(state, player) and (
        state.has("Hookshot", player) or can_fly_with_deku_leaf_indoors(state, player)
    )


def can_complete_memory_dragon_roost_cavern_and_gohma(state: CollectionState, player: int) -> bool:
    return (
        state.has("Grappling Hook", player)
        and can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_gohma(state, player)
    )


def can_complete_memory_forbidden_woods_and_kalle_demos(state: CollectionState, player: int) -> bool:
    return (
        can_fan_with_deku_leaf(state, player)
        and can_fly_with_deku_leaf_indoors(state, player)
        and can_defeat_kalle_demos(state, player)
    )


def can_complete_memory_earth_temple_and_jalhalla(state: CollectionState, player: int) -> bool:
    return can_defeat_jalhalla(state, player)


def can_complete_memory_wind_temple_and_molgera(state: CollectionState, player: int) -> bool:
    return can_fly_with_deku_leaf_indoors(state, player) and can_defeat_molgera(state, player)


def can_complete_all_memory_dungeons_and_bosses(state: CollectionState, player: int) -> bool:
    return (
        can_complete_memory_dragon_roost_cavern_and_gohma(state, player)
        and can_complete_memory_forbidden_woods_and_kalle_demos(state, player)
        and can_complete_memory_earth_temple_and_jalhalla(state, player)
        and can_complete_memory_wind_temple_and_molgera(state, player)
    )


def can_unlock_ganons_tower_four_boss_door(state: CollectionState, player: int) -> bool:
    return can_complete_all_memory_dungeons_and_bosses(state, player) or state._twwhd_rematch_bosses_skipped(player)


def can_reach_ganons_tower_phantom_ganon_room(state: CollectionState, player: int) -> bool:
    return can_access_ganons_tower(state, player) and can_unlock_ganons_tower_four_boss_door(state, player)


def can_open_ganons_tower_dark_portal(state: CollectionState, player: int) -> bool:
    return can_reach_ganons_tower_phantom_ganon_room(state, player) and state.has("Boomerang", player)


def can_reach_and_defeat_puppet_ganon(state: CollectionState, player: int) -> bool:
    return (
        can_reach_ganons_tower_phantom_ganon_room(state, player)
        and has_light_arrows(state, player)
        and can_unlock_puppet_ganon_door(state, player)
        and can_defeat_puppet_ganon(state, player)
    )


def can_unlock_puppet_ganon_door(state: CollectionState, player: int) -> bool:
    return (
        can_defeat_moblins(state, player)
        and can_defeat_mighty_darknuts(state, player)
        and (
            state._twwhd_outside_required_bosses_mode(player)
            or (state._twwhd_in_required_bosses_mode(player) and state._twwhd_can_defeat_all_required_bosses(player))
        )
    )


def can_defeat_puppet_ganon(state: CollectionState, player: int) -> bool:
    return has_light_arrows(state, player) and (state.has("Boomerang", player) or state._twwhd_precise_2(player))


def can_reach_and_defeat_ganondorf(state: CollectionState, player: int) -> bool:
    return (
        can_reach_and_defeat_puppet_ganon(state, player)
        and state.has_all(["Grappling Hook", "Hookshot"], player)
        and can_defeat_ganondorf(state, player)
    )


def can_defeat_ganondorf(state: CollectionState, player: int) -> bool:
    return (has_heros_sword(state, player) or state._twwhd_in_swordless_mode(player)) and (
        has_heros_shield(state, player) or (state.has("Skull Hammer", player) and state._twwhd_obscure_2(player))
    )


def can_farm_knights_crests(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player) and (
        # (Can Access Item Location "Ice Ring Isle - Inner Cave - Chest")
        (state.can_reach_region("Ice Ring Inner Cave", player) and has_fire_arrows(state, player))
        # | (Can Access Item Location "Outset Island - Savage Labyrinth - Floor 30")
        or (
            state.can_reach_region("Outset Savage Labyrinth", player)
            and can_defeat_keese(state, player)
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
        )
        # | (Can Access Item Location "Earth Temple - Big Key Chest" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("ET First Room", player)
            and can_reach_earth_temple_many_mirrors_room(state, player)
            and state.has("Power Bracelets", player)
            and can_play_command_melody(state, player)
            and can_aim_mirror_shield(state, player)
            and (
                can_defeat_blue_bubbles(state, player)
                or (has_heros_bow(state, player) and state._twwhd_obscure_1(player))
                or (
                    (
                        has_heros_sword(state, player)
                        or has_any_master_sword(state, player)
                        or state.has("Skull Hammer", player)
                    )
                    and state._twwhd_obscure_1(player)
                    and state._twwhd_precise_1(player)
                )
            )
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Item Location "Wind Temple - Big Key Chest" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("WT First Room", player)
            and can_reach_wind_temple_kidnapping_room(state, player)
            and state.has("Iron Boots", player)
            and can_fan_with_deku_leaf(state, player)
            and can_play_wind_gods_aria(state, player)
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Item Location "Shark Island - Cave")
        or (state.can_reach_region("Shark Island Cave", player) and can_defeat_miniblins(state, player))
        # | (Can Access Item Location "Stone Watcher Island - Cave" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("Stone Watcher Cave", player)
            and can_defeat_armos(state, player)
            and can_defeat_wizzrobes(state, player)
            and can_play_winds_requiem(state, player)
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Item Location "Overlook Island - Cave" & Can Defeat Darknuts Easily)
        or (
            state.can_reach_region("Overlook Cave", player)
            and can_defeat_stalfos(state, player)
            and can_defeat_wizzrobes(state, player)
            and can_defeat_red_chuchus(state, player)
            and can_defeat_green_chuchus(state, player)
            and can_defeat_keese(state, player)
            and can_defeat_fire_keese(state, player)
            and can_defeat_morths(state, player)
            and can_defeat_kargarocs(state, player)
            and can_play_winds_requiem(state, player)
            and can_defeat_darknuts_easily(state, player)
        )
        # | (Can Access Hyrule)
        or can_access_hyrule(state, player)
    )


def can_farm_joy_pendants(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_farm_skull_necklaces(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_farm_golden_feathers(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_farm_green_chu_jelly(state: CollectionState, player: int) -> bool:
    return state.has_all(["Grappling Hook", "Spoils Bag"], player)


def can_obtain_15_blue_chu_jelly(state: CollectionState, player: int) -> bool:
    return (
        can_get_blue_chu_jelly_from_blue_chuchus(state, player)
        and (
            state.has_any(["Hookshot", "Bombs", "Grappling Hook"], player)
            or can_move_boulders(state, player)
            or (
                can_access_secret_cave_entrance_on_shark_island(state, player)
                and can_fly_with_deku_leaf_outdoors(state, player)
            )
            or state.can_reach_region("Cliff Plateau Cave Past Wooden Barrier", player)
            or can_fan_with_deku_leaf(state, player)
            or can_access_secret_cave_entrance_on_boating_course(state, player)
        )
        and state.has("Spoils Bag", player)
    )


def can_defeat_bokoblins(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_moblins(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_darknuts(state: CollectionState, player: int) -> bool:
    return has_heros_sword(state, player) or has_light_arrows(state, player) or state.has("Skull Hammer", player)


def can_defeat_darknuts_easily(state: CollectionState, player: int) -> bool:
    return has_heros_sword(state, player) or has_light_arrows(state, player)


def can_defeat_mighty_darknuts(state: CollectionState, player: int) -> bool:
    return can_defeat_darknuts_easily(state, player) or (
        state.has("Skull Hammer", player) and state._twwhd_precise_3(player)
    )


def can_defeat_miniblins(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Grappling Hook", "Boomerang", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_miniblins_easily(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_red_chuchus(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_green_chuchus(state: CollectionState, player: int) -> bool:
    return can_defeat_red_chuchus(state, player)


def can_defeat_yellow_chuchus(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or (state.has("Boomerang", player) and has_heros_sword(state, player))
        or has_heros_bow(state, player)
        or (can_fan_with_deku_leaf(state, player) and has_heros_sword(state, player))
        or (
            state.has("Grappling Hook", player)
            and has_heros_sword(state, player)
            and state._twwhd_obscure_1(player)
            and state._twwhd_precise_2(player)
        )
    )


def can_defeat_blue_chuchus(state: CollectionState, player: int) -> bool:
    return can_defeat_yellow_chuchus(state, player)


def can_get_blue_chu_jelly_from_blue_chuchus(state: CollectionState, player: int) -> bool:
    return can_defeat_blue_chuchus(state, player) or state.has("Grappling Hook", player)


def can_defeat_keese(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Hookshot", "Grappling Hook", "Boomerang", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_fire_keese(state: CollectionState, player: int) -> bool:
    return can_defeat_keese(state, player)


def can_defeat_magtails(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Boomerang", "Hookshot", "Bombs", "Grappling Hook"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_stun_magtails(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Boomerang", "Hookshot", "Bombs", "Grappling Hook"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_kargarocs(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_peahats(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Bombs"], player)
        or (state.has("Hookshot", player) and has_heros_sword(state, player))
        or (can_fan_with_deku_leaf(state, player) and has_heros_sword(state, player))
        or has_heros_bow(state, player)
    )


def can_remove_peahat_armor(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Hookshot", "Skull Hammer", "Bombs"], player)
        or can_fan_with_deku_leaf(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_seahats(state: CollectionState, player: int) -> bool:
    return state.has_any(["Boomerang", "Hookshot", "Bombs"], player) or has_heros_bow(state, player)


def can_defeat_boko_babas(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Hookshot", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (can_fan_with_deku_leaf(state, player) and state.has("Grappling Hook", player))
    )


def can_defeat_mothulas(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_winged_mothulas(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_wizzrobes(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Hookshot", "Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_wizzrobes_at_range(state: CollectionState, player: int) -> bool:
    return has_heros_bow(state, player) or (state.has("Hookshot", player) and state._twwhd_precise_1(player))


def can_defeat_armos(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer", "Hookshot"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_big_octos(state: CollectionState, player: int) -> bool:
    return state.has_any(["Bombs", "Boomerang"], player) or has_heros_bow(state, player)


def can_defeat_12_eye_big_octos(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Boomerang"], player)
        or (has_heros_bow(state, player) and has_any_quiver_upgrade(state, player))
        or has_light_arrows(state, player)
    )


def can_defeat_red_bubbles(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (
            (can_fan_with_deku_leaf(state, player) or state.has("Hookshot", player))
            and state.has("Grappling Hook", player)
        )
    )


def can_defeat_blue_bubbles(state: CollectionState, player: int) -> bool:
    return (
        has_ice_arrows(state, player)
        or state.has("Bombs", player)
        or (
            (can_fan_with_deku_leaf(state, player) or state.has("Hookshot", player))
            and (
                state.has_any(["Grappling Hook", "Skull Hammer"], player)
                or has_heros_sword(state, player)
                or has_heros_bow(state, player)
            )
        )
    )


def can_defeat_redeads(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_light_arrows(state, player)
    )


def can_defeat_jalhalla_poes(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_stalfos(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_light_arrows(state, player)
    )


def can_defeat_floormasters(state: CollectionState, player: int) -> bool:
    return (
        has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (state.has("Skull Hammer", player) and state._twwhd_precise_1(player))
    )


def can_defeat_morths(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Hookshot"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_bombchus(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer", "Grappling Hook"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_defeat_gohma(state: CollectionState, player: int) -> bool:
    return state.has("Grappling Hook", player)


def can_defeat_kalle_demos(state: CollectionState, player: int) -> bool:
    return state.has("Boomerang", player)


def can_defeat_gohdan(state: CollectionState, player: int) -> bool:
    return (
        has_heros_bow(state, player)
        or (state.has("Hookshot", player) and state._twwhd_obscure_1(player) and state._twwhd_precise_2(player))
    ) and state.has("Bombs", player)


def can_defeat_helmaroc_king(state: CollectionState, player: int) -> bool:
    return state.has("Skull Hammer", player)


def can_defeat_jalhalla(state: CollectionState, player: int) -> bool:
    return (
        (can_aim_mirror_shield(state, player) or has_light_arrows(state, player))
        and state.has("Power Bracelets", player)
        and can_defeat_jalhalla_poes(state, player)
    )


def can_defeat_molgera(state: CollectionState, player: int) -> bool:
    return state.has("Hookshot", player) and (
        state.has_any(["Boomerang", "Grappling Hook", "Skull Hammer", "Bombs"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
    )


def can_destroy_cannons(state: CollectionState, player: int) -> bool:
    return state.has_any(["Bombs", "Boomerang"], player)


def can_cut_down_outset_trees(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Boomerang", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or (state.has("Power Bracelets", player) and state._twwhd_obscure_3(player))
    )


def can_cut_down_hanging_drc_platform(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(["Bombs", "Skull Hammer"], player)
        or has_heros_sword(state, player)
        or has_heros_bow(state, player)
        or (state.has("Hookshot", player) and state._twwhd_precise_1(player))
        or (state.has("Grappling Hook", player) and state._twwhd_precise_1(player))
    )


def can_cut_grass(state: CollectionState, player: int) -> bool:
    return state.has_any(["Skull Hammer", "Boomerang", "Bombs"], player) or has_heros_sword(state, player)


def can_sword_fight_with_orca(state: CollectionState, player: int) -> bool:
    return has_heros_sword(state, player) or state._twwhd_in_swordless_mode(player)

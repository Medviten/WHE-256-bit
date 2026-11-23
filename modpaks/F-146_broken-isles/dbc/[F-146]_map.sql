-- Written once by a scratch script (2026-11-22) for F-145..F-148's terrain-only continents; edit by hand.

-- Broken Isles (Legion's map 1220): Open Azeroth's row (F-010) at expansion 2, which a 3.3.5 account may
-- enter (the core refuses expansion 5+), and the Kalimdor loading screen (F-010's id has no LoadingScreens row)
DELETE FROM `map` WHERE `id` = 1220;
INSERT INTO `map` SET
  `id` = 1220,
  `directory` = 'Troll Raid',
  `instance_type` = 0,
  `flags` = 0,
  `pvp` = 0,
  `name_enus` = 'Broken Isles',
  `name_flags` = 16712190,
  `area_table_id` = 0,
  `desc_0_enus` = '',
  `desc_0_flags` = 16712188,
  `desc_1_enus` = '',
  `desc_1_flags` = 16712188,
  `loading_screen_id` = 3,
  `minimap_icon_scale` = 1,
  `corpse_map_id` = -1,
  `corpse_x` = 0,
  `corpse_y` = 0,
  `time_override` = -1,
  `expansion` = 2,
  `raid_offset` = 0,
  `max_players` = 0;

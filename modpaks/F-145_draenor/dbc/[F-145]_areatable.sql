-- Written once by a scratch script (2026-11-22) for F-145..F-148's terrain-only continents; edit by hand.

-- Draenor: one zone for the whole map (every tile's MCNK area id is 61145, tools/models/adt_set_area.py);
-- flyable (F-006's 0x4400). Area bit below 4096 that no other modpak uses, as of 2026-11-22
DELETE FROM `areatable` WHERE `id` = 61145;
INSERT INTO `areatable` SET
  `id` = 61145,
  `map_id` = 1116,
  `zone_id` = 0,
  `area_bit` = 4094,
  `flags` = 17408,
  `sound_provider_pref` = 0,
  `sound_provider_pref_underwater` = 0,
  `ambience` = 0,
  `zone_music` = 0,
  `zone_music_intro` = 0,
  `exploration_level` = 0,
  `name_enus` = 'Draenor',
  `name_flags` = 16712190,
  `faction_group` = 0,
  `liquid_type_1` = 0,
  `liquid_type_2` = 0,
  `liquid_type_3` = 0,
  `liquid_type_4` = 0,
  `min_elevation` = -500,
  `light_ambient_multiplier` = 0,
  `light_id` = 0;

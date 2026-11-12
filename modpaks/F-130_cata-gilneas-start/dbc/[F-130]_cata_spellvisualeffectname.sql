-- spellvisualeffectname rows ported from Cataclysm 4.0.6a (build 13623) by tools/races/cata406_dbc_port.py,
-- for F-130 (see its readme). Regenerate them with it rather than editing them here.

-- 5829 world\expansion03\doodads\worgen\items\worgen_barrel_01.mdx
DELETE FROM `spellvisualeffectname` WHERE `id` = 5829;
INSERT INTO `spellvisualeffectname` SET
  `id` = 5829,
  `name` = 'Worgen Barrel',
  `file_name` = 'world\\expansion03\\doodads\\worgen\\items\\worgen_barrel_01.mdx',
  `area_effect_size` = 0,
  `scale` = 1,
  `min_allowed_scale` = 0.1,
  `max_allowed_scale` = 10;

-- 6110 world\generic\orc\passive doodads\banners\ogrebannertiger.mdx
DELETE FROM `spellvisualeffectname` WHERE `id` = 6110;
INSERT INTO `spellvisualeffectname` SET
  `id` = 6110,
  `name` = 'Tiger Banner',
  `file_name` = 'world\\generic\\orc\\passive doodads\\banners\\ogrebannertiger.mdx',
  `area_effect_size` = 1,
  `scale` = 1,
  `min_allowed_scale` = 0.01,
  `max_allowed_scale` = 100;

-- 6902 Spells\Worgen_Combat_Transform_FX.mdx
DELETE FROM `spellvisualeffectname` WHERE `id` = 6902;
INSERT INTO `spellvisualeffectname` SET
  `id` = 6902,
  `name` = 'Worgen Combat Transform FX',
  `file_name` = 'Spells\\Worgen_Combat_Transform_FX.mdx',
  `area_effect_size` = 0,
  `scale` = 1,
  `min_allowed_scale` = 0.01,
  `max_allowed_scale` = 100;

-- 7515 particles\lootfx.mdx
DELETE FROM `spellvisualeffectname` WHERE `id` = 7515;
INSERT INTO `spellvisualeffectname` SET
  `id` = 7515,
  `name` = 'Loot FX',
  `file_name` = 'particles\\lootfx.mdx',
  `area_effect_size` = 1,
  `scale` = 0.5,
  `min_allowed_scale` = 0.01,
  `max_allowed_scale` = 100;

-- 7527 spells\blackhole_white.mdx
DELETE FROM `spellvisualeffectname` WHERE `id` = 7527;
INSERT INTO `spellvisualeffectname` SET
  `id` = 7527,
  `name` = 'White Black Hole (x2.00)',
  `file_name` = 'spells\\blackhole_white.mdx',
  `area_effect_size` = 0,
  `scale` = 2,
  `min_allowed_scale` = 0.1,
  `max_allowed_scale` = 10;

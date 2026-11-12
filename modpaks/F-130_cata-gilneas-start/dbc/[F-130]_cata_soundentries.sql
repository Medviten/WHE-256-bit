-- soundentries rows ported from Cataclysm 4.0.6a (build 13623) by tools/races/cata406_dbc_port.py,
-- for F-130 (see its readme). Regenerate them with it rather than editing them here.

-- 16417 Gilneas Cataclysm Event I (sound\event: gilneas_phase1_cc_event1.wav)
DELETE FROM `soundentries` WHERE `id` = 16417;
INSERT INTO `soundentries` SET
  `id` = 16417,
  `sound_type` = 1,
  `name` = 'Gilneas Cataclysm Event I',
  `file_1` = 'gilneas_phase1_cc_event1.wav',
  `frequency_1` = 1,
  `base_dir` = 'sound\\event',
  `volume` = 0.7,
  `flags` = 0,
  `min_distance` = 8,
  `distance_cutoff` = 45,
  `eax_def` = 0,
  `advanced_id` = 0;

-- 16426 Earthquake_Gilneas (sound\event: earthquake_gilneas.wav)
DELETE FROM `soundentries` WHERE `id` = 16426;
INSERT INTO `soundentries` SET
  `id` = 16426,
  `sound_type` = 1,
  `name` = 'Earthquake_Gilneas',
  `file_1` = 'earthquake_gilneas.wav',
  `frequency_1` = 1,
  `base_dir` = 'sound\\event',
  `volume` = 0.5,
  `flags` = 0,
  `min_distance` = 8,
  `distance_cutoff` = 45,
  `eax_def` = 0,
  `advanced_id` = 0;

-- 16427 FireBomb (Gilneas) (sound\spells: FireBomb1.wav, FireBomb2.wav, FireBomb3.wav, FireBomb4.wav)
DELETE FROM `soundentries` WHERE `id` = 16427;
INSERT INTO `soundentries` SET
  `id` = 16427,
  `sound_type` = 1,
  `name` = 'FireBomb (Gilneas)',
  `file_1` = 'FireBomb1.wav',
  `frequency_1` = 1,
  `file_2` = 'FireBomb2.wav',
  `frequency_2` = 1,
  `file_3` = 'FireBomb3.wav',
  `frequency_3` = 1,
  `file_4` = 'FireBomb4.wav',
  `frequency_4` = 1,
  `base_dir` = 'sound\\spells',
  `volume` = 0.8,
  `flags` = 0,
  `min_distance` = 30,
  `distance_cutoff` = 100,
  `eax_def` = 0,
  `advanced_id` = 0;

-- 18191 FX_RopeThrow (sound\spells: spell_uni_ropethrow_01.wav, spell_uni_ropethrow_02.wav, spell_uni_ropethrow_03.wav, spell_uni_ropethrow_04.wav, spell_uni_ropethrow_05.wav)
DELETE FROM `soundentries` WHERE `id` = 18191;
INSERT INTO `soundentries` SET
  `id` = 18191,
  `sound_type` = 1,
  `name` = 'FX_RopeThrow',
  `file_1` = 'spell_uni_ropethrow_01.wav',
  `frequency_1` = 1,
  `file_2` = 'spell_uni_ropethrow_02.wav',
  `frequency_2` = 1,
  `file_3` = 'spell_uni_ropethrow_03.wav',
  `frequency_3` = 1,
  `file_4` = 'spell_uni_ropethrow_04.wav',
  `frequency_4` = 1,
  `file_5` = 'spell_uni_ropethrow_05.wav',
  `frequency_5` = 1,
  `base_dir` = 'sound\\spells',
  `volume` = 0.8,
  `flags` = 0,
  `min_distance` = 10,
  `distance_cutoff` = 50,
  `eax_def` = 0,
  `advanced_id` = 0;

-- 19908 Worgen_Transform_Worgen (Mono) (sound\spells: worgen_transform_worgen_01.wav, worgen_transform_worgen_02.wav, worgen_transform_worgen_03.wav, worgen_transform_worgen_04.wav, worgen_transform_worgen_05.wav)
DELETE FROM `soundentries` WHERE `id` = 19908;
INSERT INTO `soundentries` SET
  `id` = 19908,
  `sound_type` = 1,
  `name` = 'Worgen_Transform_Worgen (Mono)',
  `file_1` = 'worgen_transform_worgen_01.wav',
  `frequency_1` = 1,
  `file_2` = 'worgen_transform_worgen_02.wav',
  `frequency_2` = 1,
  `file_3` = 'worgen_transform_worgen_03.wav',
  `frequency_3` = 1,
  `file_4` = 'worgen_transform_worgen_04.wav',
  `frequency_4` = 1,
  `file_5` = 'worgen_transform_worgen_05.wav',
  `frequency_5` = 1,
  `base_dir` = 'sound\\spells',
  `volume` = 0.5,
  `flags` = 0,
  `min_distance` = 8,
  `distance_cutoff` = 45,
  `eax_def` = 0,
  `advanced_id` = 0;

-- 23775 SPELL_MA_RingOfFrost_Birth (sound\spells: spell_ma_curtainfrost_impact_01.wav, spell_ma_curtainfrost_impact_02.wav, spell_ma_curtainfrost_impact_03.wav, spell_ma_curtainfrost_impact_04.wav, spell_ma_curtainfrost_impact_05.wav)
DELETE FROM `soundentries` WHERE `id` = 23775;
INSERT INTO `soundentries` SET
  `id` = 23775,
  `sound_type` = 1,
  `name` = 'SPELL_MA_RingOfFrost_Birth',
  `file_1` = 'spell_ma_curtainfrost_impact_01.wav',
  `frequency_1` = 1,
  `file_2` = 'spell_ma_curtainfrost_impact_02.wav',
  `frequency_2` = 1,
  `file_3` = 'spell_ma_curtainfrost_impact_03.wav',
  `frequency_3` = 1,
  `file_4` = 'spell_ma_curtainfrost_impact_04.wav',
  `frequency_4` = 1,
  `file_5` = 'spell_ma_curtainfrost_impact_05.wav',
  `frequency_5` = 1,
  `base_dir` = 'sound\\spells',
  `volume` = 0.85,
  `flags` = 0,
  `min_distance` = 10,
  `distance_cutoff` = 50,
  `eax_def` = 0,
  `advanced_id` = 0;

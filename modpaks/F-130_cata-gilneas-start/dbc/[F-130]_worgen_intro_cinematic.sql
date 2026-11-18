-- [F-130] Worgen character-creation intro cinematic
--
-- F-024 gives Worgen the Night Elf flythrough (@WorgenCinematicSequence = @NightElfCinematicSequence). With the
-- Gilneas start they get Cataclysm's own, over Gilneas City:
--   ChrRaces 22 -> CinematicSequences 170 -> CinematicCamera 253 (Cameras\FlyByWorgen.m2)
--   narration SoundEntries 23105 WorgenFlybyNarration -> Sound\CinematicVoices\WorgenNarration.mp3
-- Rows from the 4.0.6a DBCs. The camera's origin is Cataclysm's map 654, which Open Azeroth's Eastern Kingdoms has at the
-- same coordinates. The files (MoP Classic's copies, the camera converted with wotlkconv) are in WHE-common's patch-A.MPQ.

-- Narration: the stock race-narration volume and distances (as F-013's goblin one), not Cataclysm's 0.4 / 7 / 30
DELETE FROM `soundentries` WHERE `id` = 23105;
INSERT INTO `soundentries` SET
  `id` = 23105,
  `sound_type` = 31,
  `name` = 'WorgenFlyByNarration',
  `file_1` = 'WorgenNarration.mp3',
  `frequency_1` = 1,
  `base_dir` = 'Sound\\CinematicVoices',
  `volume` = 0.6899999976158142,
  `flags` = 0,
  `min_distance` = 8.0,
  `distance_cutoff` = 45.0,
  `eax_def` = 0,
  `advanced_id` = 0;

DELETE FROM `cinematiccamera` WHERE `id` = 253;
INSERT INTO `cinematiccamera` SET
  `id` = 253,
  `model` = 'Cameras\\FlyByWorgen.mdx',
  `sound_id` = 23105,
  `origin_x` = -1435.52001953125,
  `origin_y` = 1671.1300048828125,
  `origin_z` = 0.14964300394058228,
  `origin_facing` = 3.106689929962158;

DELETE FROM `cinematicsequences` WHERE `id` = 170;
INSERT INTO `cinematicsequences` SET
  `id` = 170,
  `sound_id` = 0,
  `camera_1` = 253,
  `camera_2` = 0,
  `camera_3` = 0,
  `camera_4` = 0,
  `camera_5` = 0,
  `camera_6` = 0,
  `camera_7` = 0,
  `camera_8` = 0;

UPDATE `chrraces` SET `cinematic_sequence_id` = 170 WHERE `id` = @Worgen;

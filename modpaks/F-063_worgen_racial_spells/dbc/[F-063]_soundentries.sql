-- Cataclysm's altered form sounds, played by the patched client when a Worgen changes form: Worgen_Transform_Human for
-- the swap without the anim, Worgen_Transform_Worgen for the human-to-Worgen anim (Cataclysm's CreatureSoundData
-- TransformSoundID and TransformAnimatedSoundID, which 3.3.5 lacks). The client finds them by these exact names, so the
-- names must not change. Values are Cataclysm's (4.3.4 ids 16448 and 16447, without their SoundEntriesAdvanced); the
-- files are in patch-A (Sound\Spells)
DELETE FROM `soundentries` WHERE `id` IN (@AlteredFormSound, @AlteredFormAnimationSound);
INSERT INTO `soundentries` (`id`, `sound_type`, `name`, `file_1`, `file_2`, `file_3`, `file_4`, `file_5`, `file_6`, `file_7`, `file_8`, `file_9`, `file_10`, `frequency_1`, `frequency_2`, `frequency_3`, `frequency_4`, `frequency_5`, `frequency_6`, `frequency_7`, `frequency_8`, `frequency_9`, `frequency_10`, `base_dir`, `volume`, `flags`, `min_distance`, `distance_cutoff`, `eax_def`, `advanced_id`) VALUES
(@AlteredFormSound,          1, '(DONOTRENAME)Altered Form Transform',          'worgen_transform_human_01.ogg', 'worgen_transform_human_02.ogg', 'worgen_transform_human_03.ogg', '', '', '', '', '', '', '', 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 'sound\\spells', 0.8, 0, 8.0, 45.0, 0, 0),
(@AlteredFormAnimationSound, 1, '(DONOTRENAME)Altered Form Transform Animated', 'worgen_transform_worgen_01.ogg', 'worgen_transform_worgen_02.ogg', 'worgen_transform_worgen_03.ogg', 'worgen_transform_worgen_04.ogg', 'worgen_transform_worgen_05.ogg', '', '', '', '', '', 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 'sound\\spells', 0.8, 0, 8.0, 45.0, 0, 0);

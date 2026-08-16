-- [F-030] mod-worgoblin: charsections
-- Preserves deleted Fel Orc entries as the new race 34

DELETE FROM `charsections` WHERE `id` = 5143;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5143, 34, 0, 0, 'Character\FelOrc\Male\FelOrcMaleSkin00_00.blp', '', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5144;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5144, 34, 0, 1, 'Character\FelOrc\Male\FelOrcMaleFaceLower00_00.blp', 'Character\FelOrc\Male\FelOrcMaleFaceUpper00_00.blp', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5145;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5145, 34, 0, 2, '', '', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5146;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5146, 34, 0, 3, 'Character\FelOrc\Hair00_00.blp', '', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5147;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5147, 34, 0, 4, 'Character\FelOrc\Male\FelOrcMaleNakedPelvisSkin00_00.blp', 'Character\FelOrc\Male\FelOrcMaleNakedTorsoSkin00_00.blp', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5148;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5148, 34, 1, 0, 'Character\FelOrc\Female\FelOrcFemaleSkin00_00.blp', '', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5149;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5149, 34, 1, 1, 'Character\FelOrc\Female\FelOrcFemaleFaceLower00_00.blp', 'Character\FelOrc\Female\FelOrcFemaleFaceUpper00_00.blp', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5150;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5150, 34, 1, 2, '', '', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5151;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5151, 34, 1, 3, 'Character\FelOrc\Hair00_01.blp', '', '', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5152;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5152, 34, 1, 4, 'Character\FelOrc\FemaleFelOrcFemaleNakedPelvisSkin00_00.blp', 'Character\FelOrc\Female\FelOrcFemaleNakedTorsoSkin00_00.blp', '', 1, 0, 0),
DELETE FROM `charsections` WHERE `id` = 5433;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5433, 34, 0, 0, 'Character\FelOrc\Male\FelOrcMaleSkin00_01.blp', '', '', 1, 0, 1),
DELETE FROM `charsections` WHERE `id` = 5434;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5434, 34, 0, 0, 'Character\FelOrc\Male\FelOrcMaleSkin00_02.blp', '', '', 1, 0, 2),
DELETE FROM `charsections` WHERE `id` = 5441;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5441, 34, 0, 1, 'Character\FelOrc\Male\FelOrcMaleFaceLower00_01.blp', 'Character\FelOrc\Male\FelOrcMaleFaceUpper00_01.blp', '', 1, 0, 1),
DELETE FROM `charsections` WHERE `id` = 5442;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5442, 34, 0, 1, 'Character\FelOrc\Male\FelOrcMaleFaceLower00_02.blp', 'Character\FelOrc\Male\FelOrcMaleFaceUpper00_02.blp', '', 1, 0, 2),
DELETE FROM `charsections` WHERE `id` = 5443;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5443, 34, 0, 4, 'Character\FelOrc\Male\FelOrcMaleNakedPelvisSkin00_01.blp', 'Character\FelOrc\Male\FelOrcMaleNakedTorsoSkin00_01.blp', '', 1, 0, 1),
DELETE FROM `charsections` WHERE `id` = 5444;
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES (5444, 34, 0, 4, 'Character\FelOrc\Male\FelOrcMaleNakedPelvisSkin00_02.blp', 'Character\FelOrc\Male\FelOrcMaleNakedTorsoSkin00_02.blp', '', 1, 0, 2);

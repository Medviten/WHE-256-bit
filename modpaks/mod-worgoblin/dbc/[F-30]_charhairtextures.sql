-- [F-30] mod-worgoblin: charhairtextures
-- Reintroduces Fel Orc entries as race 32, Naga as 33, etc.

DELETE FROM `charhairtextures` WHERE `id` = 82;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (82, 32, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 83;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (83, 32, 1, 0, 255, 0, 0, 0);
DELETE FROM `charhairtextures` WHERE `id` = 84;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (84, 33, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 85;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (85, 33, 1, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 86;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (86, 34, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 87;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (87, 34, 1, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 89;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (89, 35, 1, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 88;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (88, 35, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 90;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (90, 36, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 91;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (91, 36, 1, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 92;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (92, 37, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 93;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (93, 37, 1, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 98;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (98, 38, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 99;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (99, 38, 1, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 100;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (100, 39, 0, 0, 255, 0, 1, 1);
DELETE FROM `charhairtextures` WHERE `id` = 101;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES (101, 39, 1, 0, 255, 0, 1, 1);

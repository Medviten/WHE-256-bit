-- [F-30] mod-worgoblin: creaturedisplayinfoextra
-- Moving Skeleton entry to the new race ID (25)

DELETE FROM `vocaluisounds` WHERE `id` = 848;
INSERT INTO `vocaluisounds` (`id`, `vocal_ui_enum`, `race_id`, `normal_sound_id_1`, `normal_sound_id_2`, `pissed_sound_id_1`, `pissed_sound_id_2`) VALUES (848, 0, 25, 0, 0, 0, 0);

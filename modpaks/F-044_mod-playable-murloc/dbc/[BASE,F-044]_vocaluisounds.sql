-- vocaluisounds: one insert per Troll row, 0 updates, 0 deletes
-- Murlocs have no player voice: every error the Troll voices gets the murloc alert sound instead (rows the Troll leaves
-- silent stay silent).

-- New entries
DELETE FROM `vocaluisounds` WHERE `race_id` = @Murloc;
SET @VocalUISoundsID = (SELECT COALESCE(MAX(id), 0) FROM `vocaluisounds`);
INSERT INTO `vocaluisounds` (`id`, `vocal_ui_enum`, `race_id`, `normal_sound_id_1`, `normal_sound_id_2`, `pissed_sound_id_1`, `pissed_sound_id_2`)
SELECT @VocalUISoundsID := @VocalUISoundsID +1, `t`.`vocal_ui_enum`, @Murloc,
       IF(`t`.`normal_sound_id_1` IN (0, 4294967295), `t`.`normal_sound_id_1`, @MurlocVoiceSound),
       IF(`t`.`normal_sound_id_2` IN (0, 4294967295), `t`.`normal_sound_id_2`, @MurlocVoiceSound),
       0, 0
FROM (SELECT * FROM `vocaluisounds` WHERE `race_id` = @Troll) AS `t`
ORDER BY `t`.`id`;

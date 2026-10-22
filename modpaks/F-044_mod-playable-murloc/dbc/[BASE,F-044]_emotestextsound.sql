-- emotestextsound: one insert per Troll row, 0 updates, 0 deletes
-- Murlocs have no player voice: every emote the Troll voices gets the murloc aggro gurgle instead.

-- New entries
DELETE FROM `emotestextsound` WHERE `race_id` = @Murloc;
SET @EmotesTextSoundID = (SELECT COALESCE(MAX(id), 0) FROM `emotestextsound`);
INSERT INTO `emotestextsound` (`id`, `emotes_text_id`, `race_id`, `sex_id`, `sound_id`)
SELECT @EmotesTextSoundID := @EmotesTextSoundID +1, `t`.`emotes_text_id`, @Murloc, `t`.`sex_id`, @MurlocEmoteSound
FROM (SELECT * FROM `emotestextsound` WHERE `race_id` = @Troll) AS `t`
ORDER BY `t`.`id`;

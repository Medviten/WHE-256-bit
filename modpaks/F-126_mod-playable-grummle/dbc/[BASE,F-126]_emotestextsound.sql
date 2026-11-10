-- emotestextsound: the emote sounds of @GrummleKin (kin)

DELETE FROM `emotestextsound` WHERE `race_id` = @Grummle;
SET @EmotesTextSoundID = (SELECT COALESCE(MAX(id), 0) FROM `emotestextsound`);
INSERT INTO `emotestextsound` (`id`, `emotes_text_id`, `race_id`, `sex_id`, `sound_id`)
SELECT @EmotesTextSoundID := @EmotesTextSoundID +1, `emotes_text_id`, @Grummle, `sex_id`, `sound_id`
FROM (SELECT * FROM `emotestextsound` WHERE `race_id` = @GrummleKin ORDER BY `id`) AS `kin`;

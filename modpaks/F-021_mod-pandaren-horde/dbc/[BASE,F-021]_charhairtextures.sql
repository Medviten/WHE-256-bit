-- charhairtextures: the Neutral Pandaren rows of F-129, for this race
DELETE FROM `charhairtextures` WHERE `race` = @HordePandaren;
SET @CharHairTexturesID = (SELECT COALESCE(MAX(`id`), 0) FROM `charhairtextures`);
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`)
SELECT @CharHairTexturesID := @CharHairTexturesID + 1, @HordePandaren, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`
FROM (SELECT * FROM `charhairtextures` WHERE `race` = @NeutralPandaren) AS `n`;

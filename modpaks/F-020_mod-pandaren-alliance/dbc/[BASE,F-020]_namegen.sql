-- namegen: the Neutral Pandaren rows of F-129, for this race
DELETE FROM `namegen` WHERE `race_id` = @AlliancePandaren;
SET @NameGenID = (SELECT COALESCE(MAX(`id`), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID + 1, `name`, @AlliancePandaren, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @NeutralPandaren) AS `n`;

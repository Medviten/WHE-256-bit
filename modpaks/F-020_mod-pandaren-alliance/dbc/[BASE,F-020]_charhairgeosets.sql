-- charhairgeosets: the Neutral Pandaren rows of F-129, for this race
DELETE FROM `charhairgeosets` WHERE `race` = @AlliancePandaren;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(`id`), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`)
SELECT @CharHairGeosetsID := @CharHairGeosetsID + 1, @AlliancePandaren, `gender`, `variation`, `geoset`, `show_scalp`
FROM (SELECT * FROM `charhairgeosets` WHERE `race` = @NeutralPandaren) AS `n`;

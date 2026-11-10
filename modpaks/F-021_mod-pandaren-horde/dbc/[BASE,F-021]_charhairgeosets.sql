-- charhairgeosets: the Neutral Pandaren rows of F-129, for this race
DELETE FROM `charhairgeosets` WHERE `race` = @HordePandaren;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(`id`), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`)
SELECT @CharHairGeosetsID := @CharHairGeosetsID + 1, @HordePandaren, `gender`, `variation`, `geoset`, `show_scalp`
FROM (SELECT * FROM `charhairgeosets` WHERE `race` = @NeutralPandaren) AS `n`;

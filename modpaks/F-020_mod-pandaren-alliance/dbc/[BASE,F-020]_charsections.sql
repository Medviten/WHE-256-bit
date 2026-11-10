-- charsections: the Neutral Pandaren rows of F-129, for this race
DELETE FROM `charsections` WHERE `race` = @AlliancePandaren;
SET @CharSectionsID = (SELECT COALESCE(MAX(`id`), 0) FROM `charsections`);
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`)
SELECT @CharSectionsID := @CharSectionsID + 1, @AlliancePandaren, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`
FROM (SELECT * FROM `charsections` WHERE `race` = @NeutralPandaren) AS `n`;

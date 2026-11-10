-- namegen: the random names of @AllianceOrcKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @AllianceOrc;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @AllianceOrc, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @AllianceOrcKin ORDER BY `id`) AS `kin`;

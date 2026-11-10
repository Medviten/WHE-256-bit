-- namegen: the random names of @SporelingKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Sporeling;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Sporeling, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @SporelingKin ORDER BY `id`) AS `kin`;

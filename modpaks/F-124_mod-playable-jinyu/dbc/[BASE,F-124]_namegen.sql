-- namegen: the random names of @JinyuKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Jinyu;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Jinyu, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @JinyuKin ORDER BY `id`) AS `kin`;

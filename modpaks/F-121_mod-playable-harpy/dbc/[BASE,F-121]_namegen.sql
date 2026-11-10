-- namegen: the random names of @HarpyKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Harpy;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Harpy, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @HarpyKin ORDER BY `id`) AS `kin`;

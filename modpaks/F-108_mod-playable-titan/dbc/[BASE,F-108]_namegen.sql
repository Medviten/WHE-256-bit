-- namegen: the random names of @TitanKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Titan;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Titan, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @TitanKin ORDER BY `id`) AS `kin`;

-- namegen: the random names of @StormforgedKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Stormforged;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Stormforged, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @StormforgedKin ORDER BY `id`) AS `kin`;

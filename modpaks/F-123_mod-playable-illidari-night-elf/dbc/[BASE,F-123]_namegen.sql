-- namegen: the random names of @IllidariNightElfKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @IllidariNightElf;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @IllidariNightElf, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @IllidariNightElfKin ORDER BY `id`) AS `kin`;

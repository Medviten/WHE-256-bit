-- namegen: the random names of @IllidariBloodElfKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @IllidariBloodElf;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @IllidariBloodElf, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @IllidariBloodElfKin ORDER BY `id`) AS `kin`;

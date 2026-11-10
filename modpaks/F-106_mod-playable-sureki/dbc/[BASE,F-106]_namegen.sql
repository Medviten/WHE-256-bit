-- namegen: the random names of @SurekiKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Sureki;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Sureki, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @SurekiKin ORDER BY `id`) AS `kin`;

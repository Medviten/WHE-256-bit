-- namegen: the random names of @FungarianKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Fungarian;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Fungarian, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @FungarianKin ORDER BY `id`) AS `kin`;

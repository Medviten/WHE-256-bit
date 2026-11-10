-- namegen: the random names of @LichKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Lich;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Lich, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @LichKin ORDER BY `id`) AS `kin`;

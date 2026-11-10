-- namegen: the random names of @SethrakKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Sethrak;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Sethrak, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @SethrakKin ORDER BY `id`) AS `kin`;

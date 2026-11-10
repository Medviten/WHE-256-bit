-- namegen: the random names of @MoguKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Mogu;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Mogu, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @MoguKin ORDER BY `id`) AS `kin`;

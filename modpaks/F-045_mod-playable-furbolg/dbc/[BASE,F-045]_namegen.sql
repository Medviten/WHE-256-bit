-- namegen: the random names of @Tauren (kin)

DELETE FROM `namegen` WHERE `race_id` = @Furbolg;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Furbolg, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @Tauren ORDER BY `id`) AS `kin`;

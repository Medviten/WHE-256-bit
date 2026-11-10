-- namegen: the random names of @NerubianKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Nerubian;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Nerubian, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @NerubianKin ORDER BY `id`) AS `kin`;

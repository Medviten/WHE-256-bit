-- namegen: the random names of @DrakkinKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Drakkin;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Drakkin, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @DrakkinKin ORDER BY `id`) AS `kin`;

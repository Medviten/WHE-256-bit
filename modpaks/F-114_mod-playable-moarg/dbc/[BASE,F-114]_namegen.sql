-- namegen: the random names of @MoargKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Moarg;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Moarg, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @MoargKin ORDER BY `id`) AS `kin`;

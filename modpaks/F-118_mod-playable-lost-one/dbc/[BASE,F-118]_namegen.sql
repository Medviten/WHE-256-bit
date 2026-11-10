-- namegen: the random names of @LostOneKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @LostOne;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @LostOne, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @LostOneKin ORDER BY `id`) AS `kin`;

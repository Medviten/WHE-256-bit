-- namegen: the random names of @DrakonidKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Drakonid;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Drakonid, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @DrakonidKin ORDER BY `id`) AS `kin`;

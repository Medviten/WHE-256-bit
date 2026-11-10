-- namegen: the random names of @GrummleKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @Grummle;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @Grummle, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @GrummleKin ORDER BY `id`) AS `kin`;

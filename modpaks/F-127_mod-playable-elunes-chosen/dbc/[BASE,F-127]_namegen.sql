-- namegen: the random names of @EluneChosenKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @EluneChosen;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @EluneChosen, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @EluneChosenKin ORDER BY `id`) AS `kin`;

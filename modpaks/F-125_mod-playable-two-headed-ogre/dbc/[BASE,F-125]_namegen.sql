-- namegen: the random names of @TwoHeadedOgreKin (kin)

DELETE FROM `namegen` WHERE `race_id` = @TwoHeadedOgre;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`)
SELECT @NameGenID := @NameGenID +1, `name`, @TwoHeadedOgre, `sex`
FROM (SELECT * FROM `namegen` WHERE `race_id` = @TwoHeadedOgreKin ORDER BY `id`) AS `kin`;

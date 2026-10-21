-- Start positions of @TuskarrHome
DELETE FROM `playercreateinfo` WHERE `race` = @Tuskarr;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @Tuskarr, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`
FROM (SELECT * FROM `playercreateinfo` WHERE `race` = @TuskarrHome) AS `home`;

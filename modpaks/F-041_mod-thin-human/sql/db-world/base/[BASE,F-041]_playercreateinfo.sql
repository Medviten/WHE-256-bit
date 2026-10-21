-- Start positions of @ThinHumanHome
DELETE FROM `playercreateinfo` WHERE `race` = @ThinHuman;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @ThinHuman, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`
FROM (SELECT * FROM `playercreateinfo` WHERE `race` = @ThinHumanHome) AS `home`;

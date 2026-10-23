-- Start positions of @FurbolgHome
DELETE FROM `playercreateinfo` WHERE `race` = @Furbolg;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @Furbolg, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`
FROM (SELECT * FROM `playercreateinfo` WHERE `race` = @FurbolgHome) AS `home`;

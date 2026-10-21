-- Start positions of @MechagnomeHome
DELETE FROM `playercreateinfo` WHERE `race` = @Mechagnome;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @Mechagnome, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`
FROM (SELECT * FROM `playercreateinfo` WHERE `race` = @MechagnomeHome) AS `home`;

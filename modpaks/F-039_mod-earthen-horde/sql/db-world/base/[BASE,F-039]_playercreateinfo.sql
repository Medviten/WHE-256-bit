-- Start positions of @HordeEarthenHome
DELETE FROM `playercreateinfo` WHERE `race` = @HordeEarthen;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @HordeEarthen, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`
FROM (SELECT * FROM `playercreateinfo` WHERE `race` = @HordeEarthenHome) AS `home`;

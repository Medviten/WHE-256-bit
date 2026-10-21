-- Start positions of @AllianceEarthenHome
DELETE FROM `playercreateinfo` WHERE `race` = @AllianceEarthen;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @AllianceEarthen, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`
FROM (SELECT * FROM `playercreateinfo` WHERE `race` = @AllianceEarthenHome) AS `home`;

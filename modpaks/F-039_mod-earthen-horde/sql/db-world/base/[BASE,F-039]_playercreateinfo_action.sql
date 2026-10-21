-- Action bars of @HordeEarthenHome
DELETE FROM `playercreateinfo_action` WHERE `race` = @HordeEarthen;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT @HordeEarthen, `class`, `button`, `action`, `type`
FROM (SELECT * FROM `playercreateinfo_action` WHERE `race` = @HordeEarthenHome) AS `home`;

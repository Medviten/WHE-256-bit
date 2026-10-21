-- Action bars of @AllianceEarthenHome
DELETE FROM `playercreateinfo_action` WHERE `race` = @AllianceEarthen;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT @AllianceEarthen, `class`, `button`, `action`, `type`
FROM (SELECT * FROM `playercreateinfo_action` WHERE `race` = @AllianceEarthenHome) AS `home`;

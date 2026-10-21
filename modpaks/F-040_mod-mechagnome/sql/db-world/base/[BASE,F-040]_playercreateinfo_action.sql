-- Action bars of @MechagnomeHome
DELETE FROM `playercreateinfo_action` WHERE `race` = @Mechagnome;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT @Mechagnome, `class`, `button`, `action`, `type`
FROM (SELECT * FROM `playercreateinfo_action` WHERE `race` = @MechagnomeHome) AS `home`;

-- Action bars of @ThinHumanHome
DELETE FROM `playercreateinfo_action` WHERE `race` = @ThinHuman;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT @ThinHuman, `class`, `button`, `action`, `type`
FROM (SELECT * FROM `playercreateinfo_action` WHERE `race` = @ThinHumanHome) AS `home`;

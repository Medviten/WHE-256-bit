-- Action bars of @FurbolgHome
DELETE FROM `playercreateinfo_action` WHERE `race` = @Furbolg;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT @Furbolg, `class`, `button`, `action`, `type`
FROM (SELECT * FROM `playercreateinfo_action` WHERE `race` = @FurbolgHome) AS `home`;

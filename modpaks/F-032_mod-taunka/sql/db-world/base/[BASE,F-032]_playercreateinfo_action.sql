DELETE FROM `playercreateinfo_action` WHERE `race` = @Taunka;
INSERT INTO `playercreateinfo_action` (`race`,`class`,`button`,`action`,`type`)
SELECT @Taunka,`class`,`button`,`action`,`type` FROM `playercreateinfo_action` WHERE `race` = @Tauren;

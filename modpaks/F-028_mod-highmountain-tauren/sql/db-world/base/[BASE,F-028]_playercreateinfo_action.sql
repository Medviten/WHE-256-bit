DELETE FROM `playercreateinfo_action` WHERE `race` = @HighmountainTauren;
INSERT INTO `playercreateinfo_action` (`race`,`class`,`button`,`action`,`type`)
SELECT @HighmountainTauren,`class`,`button`,`action`,`type` FROM `playercreateinfo_action` WHERE `race` = @Tauren;

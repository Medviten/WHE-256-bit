DELETE FROM `playercreateinfo_action` WHERE `race` = @Naga;
INSERT INTO `playercreateinfo_action` (`race`,`class`,`button`,`action`,`type`)
SELECT @Naga,`class`,`button`,`action`,`type` FROM `playercreateinfo_action` WHERE `race` = @BloodElf;

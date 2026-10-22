/* Murlocs get the Troll action bars */
DELETE FROM `playercreateinfo_action` WHERE `race` = @Murloc;
INSERT INTO `playercreateinfo_action` (`race`,`class`,`button`,`action`,`type`)
SELECT @Murloc,`class`,`button`,`action`,`type` FROM `playercreateinfo_action` WHERE `race` = @Troll;

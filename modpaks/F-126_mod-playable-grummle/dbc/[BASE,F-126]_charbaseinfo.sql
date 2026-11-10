-- charbaseinfo: the classes of @GrummleHome

DELETE FROM `charbaseinfo` WHERE `race` = @Grummle;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Grummle, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @GrummleHome) AS `home`;

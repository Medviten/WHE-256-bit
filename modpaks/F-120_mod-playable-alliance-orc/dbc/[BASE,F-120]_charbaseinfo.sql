-- charbaseinfo: the classes of @AllianceOrcHome

DELETE FROM `charbaseinfo` WHERE `race` = @AllianceOrc;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @AllianceOrc, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @AllianceOrcHome) AS `home`;

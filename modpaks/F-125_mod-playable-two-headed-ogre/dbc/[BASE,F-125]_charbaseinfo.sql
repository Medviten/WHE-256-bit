-- charbaseinfo: the classes of @TwoHeadedOgreHome

DELETE FROM `charbaseinfo` WHERE `race` = @TwoHeadedOgre;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @TwoHeadedOgre, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @TwoHeadedOgreHome) AS `home`;

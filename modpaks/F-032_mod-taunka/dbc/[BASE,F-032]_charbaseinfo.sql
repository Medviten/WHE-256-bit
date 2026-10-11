-- charbaseinfo: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Taunka;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Taunka, @Warrior),
(@Taunka, @Hunter),
(@Taunka, @DeathKnight),
(@Taunka, @Shaman),
(@Taunka, @Druid);

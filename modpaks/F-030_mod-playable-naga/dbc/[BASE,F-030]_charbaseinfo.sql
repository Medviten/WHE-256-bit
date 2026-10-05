-- charbaseinfo: 10 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Naga;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Naga, @Warrior),
(@Naga, @Paladin),
(@Naga, @Hunter),
(@Naga, @Rogue),
(@Naga, @Priest),
(@Naga, @DeathKnight),
(@Naga, @Shaman),
(@Naga, @Mage),
(@Naga, @Warlock),
(@Naga, @Druid);

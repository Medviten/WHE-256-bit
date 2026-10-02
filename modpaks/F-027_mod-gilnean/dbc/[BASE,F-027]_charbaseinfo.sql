-- charbaseinfo: 16 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Gilnean;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Gilnean, @Warrior),
(@Gilnean, @Hunter),
(@Gilnean, @Rogue),
(@Gilnean, @Priest),
(@Gilnean, @DeathKnight),
(@Gilnean, @Mage),
(@Gilnean, @Warlock),
(@Gilnean, @Druid);

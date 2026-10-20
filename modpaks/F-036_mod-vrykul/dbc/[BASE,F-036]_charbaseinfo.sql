-- charbaseinfo: 10 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Vrykul;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Vrykul, @Warrior),
(@Vrykul, @Paladin),
(@Vrykul, @Hunter),
(@Vrykul, @Rogue),
(@Vrykul, @Priest),
(@Vrykul, @DeathKnight),
(@Vrykul, @Shaman),
(@Vrykul, @Mage),
(@Vrykul, @Warlock),
(@Vrykul, @Druid);

-- charbaseinfo: 7 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Nightborne;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Nightborne, @Warrior),
(@Nightborne, @Hunter),
(@Nightborne, @Rogue),
(@Nightborne, @Priest),
(@Nightborne, @DeathKnight),
(@Nightborne, @Mage),
(@Nightborne, @Warlock);

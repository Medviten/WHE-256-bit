-- charbaseinfo: 7 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @VoidElf;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@VoidElf, @Warrior),
(@VoidElf, @Hunter),
(@VoidElf, @Rogue),
(@VoidElf, @Priest),
(@VoidElf, @DeathKnight),
(@VoidElf, @Mage),
(@VoidElf, @Warlock);

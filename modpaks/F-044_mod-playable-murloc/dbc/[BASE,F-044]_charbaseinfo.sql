-- charbaseinfo: 4 inserts, 0 updates, 0 deletes (donor client classes)

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Murloc;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Murloc, @Warrior),
(@Murloc, @Rogue),
(@Murloc, @Shaman),
(@Murloc, @Mage);

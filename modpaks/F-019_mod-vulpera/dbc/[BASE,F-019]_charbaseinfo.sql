-- charbaseinfo: 8 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Vulpera;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Vulpera, @Warrior),
(@Vulpera, @Hunter),
(@Vulpera, @Rogue),
(@Vulpera, @Priest),
(@Vulpera, @DeathKnight),
(@Vulpera, @Shaman),
(@Vulpera, @Mage),
(@Vulpera, @Warlock);

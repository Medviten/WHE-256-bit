-- charbaseinfo: 9 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @HighmountainTauren;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@HighmountainTauren, @Warrior),
(@HighmountainTauren, @Hunter),
(@HighmountainTauren, @Rogue),
(@HighmountainTauren, @Priest),
(@HighmountainTauren, @DeathKnight),
(@HighmountainTauren, @Shaman),
(@HighmountainTauren, @Mage),
(@HighmountainTauren, @Warlock),
(@HighmountainTauren, @Druid);

-- [F-043] mod-darkfallen: charbaseinfo: 8 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @Darkfallen;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@Darkfallen, @Warrior),
(@Darkfallen, @Paladin),
(@Darkfallen, @Hunter),
(@Darkfallen, @Rogue),
(@Darkfallen, @Priest),
(@Darkfallen, @DeathKnight),
(@Darkfallen, @Mage),
(@Darkfallen, @Warlock);

-- charbaseinfo: 9 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = @LightforgedDraenei;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES
(@LightforgedDraenei, @Warrior),
(@LightforgedDraenei, @Paladin),
(@LightforgedDraenei, @Hunter),
(@LightforgedDraenei, @Rogue),
(@LightforgedDraenei, @Priest),
(@LightforgedDraenei, @DeathKnight),
(@LightforgedDraenei, @Mage),
(@LightforgedDraenei, @Warlock),
(@LightforgedDraenei, @Druid);

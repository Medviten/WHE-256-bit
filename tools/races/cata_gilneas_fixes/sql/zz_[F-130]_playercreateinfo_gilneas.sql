-- [F-130] Worgen starting zone -> Gilneas City
--
-- New Worgen characters, except Death Knights, start where Neltharion (and Cataclysm) put them: Gilneas City, by
-- Prince Liam Greymane, who offers the first quest, "Lockdown!" (14078). Cataclysm's map 654 is at the same
-- coordinates as Open Azeroth's Eastern Kingdoms, so only the map changes. Their first hearthstone bind is here too:
-- the server falls back to playercreateinfo when a character has no character_homebind row.
--
-- playercreateinfo is only read at startup: restart the worldserver after applying.

UPDATE `playercreateinfo` SET
  `map` = @EasternKingdoms,
  `zone` = 4755,
  `position_x` = -1451.64,
  `position_y` = 1403.36,
  `position_z` = 35.5561,
  `orientation` = 0.353427
WHERE `race` = @Worgen AND `class` <> @DeathKnight;

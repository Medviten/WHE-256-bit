/* Murlocs copy Troll stats */
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT
  @Murloc, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM `player_race_stats` AS src
WHERE src.Race = @Troll
  AND NOT EXISTS (
    SELECT 1 FROM `player_race_stats` WHERE `Race` = @Murloc
  );

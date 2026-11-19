-- F-137 Exile's Reach as a start zone: races whose player_race_template row has exiles_reach = 1 (F-091's default;
-- the race modpaks that keep their home race's start set 0, and stock races have no row or 0) start on the island's
-- beach, where retail's crash lands its players (TrinityCore's spells 305425 / 325131). Death Knights keep Acherus.
-- With ExilesReachStartZone.Enable on, the core boards them on their faction's ship instead (exiles_reach_start.cpp);
-- with the Wandering Isle start on, the races it takes (Pandaren and the races starting with them) go there on their
-- first login. Hand-written; runs after every race modpak's playercreateinfo (F-137 comes late in the manifest).
UPDATE `playercreateinfo` AS `p`
JOIN `player_race_template` AS `t` ON `t`.`race` = `p`.`race`
SET `p`.`map` = 2175, `p`.`zone` = 10424, `p`.`position_x` = -462.4, `p`.`position_y` = -2619.8,
    `p`.`position_z` = 0.4, `p`.`orientation` = 0.53
WHERE `t`.`exiles_reach` = 1 AND `p`.`class` <> 6;

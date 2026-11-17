-- [F-132] shaman-totems: another race's totem set for a stock race (the totem counterpart of F-011's druid forms).
-- Each row only goes in when its display's model is the one named (so the race modpak that brings it is installed);
-- otherwise the race keeps what it had, or gets F-026's side default.
REPLACE INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`)
SELECT `t`.`TotemID`, `t`.`RaceID`, `t`.`ModelID`
FROM (
    -- Gnome: Goblin totems (F-023_mod-playable-goblin)
    SELECT 1 AS `TotemID`, @Gnome AS `RaceID`, @GoblinFireTotem AS `ModelID`, 'GoblinShamanTotem_Fire' AS `Model`
    UNION ALL SELECT 2, @Gnome, @GoblinEarthTotem, 'GoblinShamanTotem_Earth'
    UNION ALL SELECT 3, @Gnome, @GoblinWaterTotem, 'GoblinShamanTotem_Water'
    UNION ALL SELECT 4, @Gnome, @GoblinAirTotem, 'GoblinShamanTotem_Air'
) AS `t`
JOIN `dbc_db`.`creaturedisplayinfo` AS `d` ON `d`.`id` = `t`.`ModelID`
JOIN `dbc_db`.`creaturemodeldata` AS `m` ON `m`.`id` = `d`.`model_id` AND `m`.`model_path` LIKE CONCAT('%', `t`.`Model`, '%')
WHERE `t`.`RaceID` IS NOT NULL; -- races that aren't in this build have no ID

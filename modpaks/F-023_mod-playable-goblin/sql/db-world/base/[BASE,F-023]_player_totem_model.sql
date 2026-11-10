-- Goblin: Cataclysm's goblin totems (dbc/[F-023]_cata_totems.sql; the models are in WHE-common). Without this the
-- race would get F-026's Horde default (the Orc totems).
DELETE FROM `player_totem_model` WHERE `RaceID` = @Goblin;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @Goblin, @GoblinFireTotem),
(2, @Goblin, @GoblinEarthTotem),
(3, @Goblin, @GoblinWaterTotem),
(4, @Goblin, @GoblinAirTotem);

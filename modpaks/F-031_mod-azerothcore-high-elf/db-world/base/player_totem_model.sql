-- Alliance default totems is the Dwarf ones
SET @HighElfFireTotem := 30754;
SET @HighElfEarthTotem := 30753;
SET @HighElfWaterTotem := 30755;
SET @HighElfAirTotem := 30736;

-- Human, Night Elf, Undead, Gnome, Goblin, Blood Elf, Worgen, High Elf, and Mag'har Orc
DELETE FROM player_totem_model WHERE RaceID IN (13);
INSERT INTO player_totem_model (TotemID, RaceID, ModelID) VALUES 
(1, 13, @HighElfFireTotem),
(2, 13, @HighElfEarthTotem),
(3, 13, @HighElfWaterTotem),
(4, 13, @HighElfAirTotem);

-- Horde default totems is the Orc ones.
SET @MagharOrcFireTotem := 30758;
SET @MagharOrcEarthTotem := 30757;
SET @MagharOrcWaterTotem := 30759;
SET @MagharOrcAirTotem := 30756;

-- Mag'har Orc
DELETE FROM player_totem_model WHERE RaceID IN (14);
INSERT INTO player_totem_model (TotemID, RaceID, ModelID) VALUES 
(1, 14, @MagharOrcFireTotem),
(2, 14, @MagharOrcEarthTotem),
(3, 14, @MagharOrcWaterTotem),
(4, 14, @MagharOrcAirTotem);


-- Horde default totems is the Orc ones.
SET @OgreFireTotem := 30758;
SET @OgreEarthTotem := 30757;
SET @OgreWaterTotem := 30759;
SET @OgreAirTotem := 30756;

-- Ogre
DELETE FROM player_totem_model WHERE RaceID IN (15);
INSERT INTO player_totem_model (TotemID, RaceID, ModelID) VALUES 
(1, 15, @OgreFireTotem),
(2, 15, @OgreEarthTotem),
(3, 15, @OgreWaterTotem),
(4, 15, @OgreAirTotem);


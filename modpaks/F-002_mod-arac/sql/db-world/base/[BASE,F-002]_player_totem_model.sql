/* Probably not needed anymore because of F-026.
-- Adds totems for races that don't have them.
DELETE FROM `player_totem_model` WHERE `RaceID` IN (@Human, @NightElf, @Undead, @Gnome, @BloodElf);
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES 
(1, @Human,    @AllianceFireTotem),
(2, @Human,    @AllianceEarthTotem),
(3, @Human,    @AllianceWaterTotem),
(4, @Human,    @AllianceAirTotem),
(1, @NightElf, @AllianceFireTotem),
(2, @NightElf, @AllianceEarthTotem),
(3, @NightElf, @AllianceWaterTotem),
(4, @NightElf, @AllianceAirTotem),
(1, @Undead,   @HordeFireTotem),
(2, @Undead,   @HordeEarthTotem),
(3, @Undead,   @HordeWaterTotem),
(4, @Undead,   @HordeAirTotem),
(1, @Gnome,    @AllianceFireTotem),
(2, @Gnome,    @AllianceEarthTotem),
(3, @Gnome,    @AllianceWaterTotem),
(4, @Gnome,    @AllianceAirTotem),
(1, @BloodElf, @HordeFireTotem),
(2, @BloodElf, @HordeEarthTotem),
(3, @BloodElf, @HordeWaterTotem),
(4, @BloodElf, @HordeAirTotem);
*/
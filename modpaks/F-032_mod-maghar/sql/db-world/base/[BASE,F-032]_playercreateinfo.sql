SET @MagharOrc        =   14;
SET @Warrior          =    1;
SET @Paladin          =    2;
SET @Hunter           =    3;
SET @Rogue            =    4;
SET @Priest           =    5;
SET @DeathKnight      =    6;
SET @Shaman           =    7;
SET @Mage             =    8;
SET @Warlock          =    9;
SET @Druid            =   11;
SET @Kalimdor         =    1;
SET @Durotar          =   14;
SET @Northrend        =  609;
SET @ScarletEnclave   = 4298;
INSERT IGNORE INTO `playercreateinfo` VALUES
/* Mag'har Orc starting zone (Durotar) */
(@MagharOrc, @Warrior, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Mag'har Orc Warrior
(@MagharOrc, @Paladin, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Mag'har Orc Paladin (ARAC)
(@MagharOrc, @Hunter, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Mag'har Orc Hunter
(@MagharOrc, @Rogue, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Mag'har Orc Rogue
(@MagharOrc, @Priest, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Mag'har Orc Priest
(@MagharOrc, @DeathKnight, @Northrend, @ScarletEnclave, 2358.44, -5666.9, 426.023, 3.65997), -- Mag'har Orc Death Knight
(@MagharOrc, @Shaman, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Mag'har Orc Shaman
(@MagharOrc, @Mage, @Kalimdor, @Durotar, -618.518, -4215.67, 38.718, 0), -- Mag'har Orc Mage
(@MagharOrc, @Warlock, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Mag'har Orc Warlock
(@MagharOrc, @Druid, @Kalimdor, @Durotar, -618.518, -4215.67, 38.718, 0); -- Mag'har Orc Druid (ARAC)

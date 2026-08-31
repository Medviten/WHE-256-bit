SET @Ogre          =      15;
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
/* Ogre starting zone (Durotar) */
(@Ogre, @Warrior, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Ogre Warrior
(@Ogre, @Paladin, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Ogre Paladin (ARAC)
(@Ogre, @Hunter, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Ogre Hunter
(@Ogre, @Rogue, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Ogre Rogue (ARAC)
(@Ogre, @Priest, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Ogre Priest (ARAC)
(@Ogre, @DeathKnight, @Northrend, @ScarletEnclave, 2358.44, -5666.9, 426.023, 3.65997), -- Ogre Death Knight (ARAC)
(@Ogre, @Shaman, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Ogre Shaman
(@Ogre, @Mage, @Kalimdor, @Durotar, -618.518, -4215.67, 38.718, 0), -- Ogre Mage
(@Ogre, @Warlock, @Kalimdor, @Durotar, -618.518, -4251.67, 38.718, 0), -- Ogre Warlock
(@Ogre, @Druid, @Kalimdor, @Durotar, -618.518, -4215.67, 38.718, 0); -- Ogre Druid (ARAC)

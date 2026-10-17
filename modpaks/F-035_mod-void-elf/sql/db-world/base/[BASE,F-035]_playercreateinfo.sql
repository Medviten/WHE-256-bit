DELETE FROM `playercreateinfo` WHERE `race` = @VoidElf;
INSERT IGNORE INTO `playercreateinfo` VALUES
(@VoidElf, @Warrior,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@VoidElf, @Paladin,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@VoidElf, @Hunter,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@VoidElf, @Rogue,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@VoidElf, @Priest,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@VoidElf, @Shaman,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@VoidElf, @Mage,        @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@VoidElf, @Warlock,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@VoidElf, @Druid,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@VoidElf, @DeathKnight, @Northrend, @ScarletEnclave,  @DKStartX,        @DKStartY,       @DKStartZ,       @DKStartO);

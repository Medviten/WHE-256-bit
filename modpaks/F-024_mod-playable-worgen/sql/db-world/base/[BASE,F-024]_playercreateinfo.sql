DELETE FROM `playercreateinfo` WHERE `race` = @Worgen;
INSERT IGNORE INTO `playercreateinfo` VALUES
(@Worgen, @Warrior,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Paladin,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@Worgen, @Hunter,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Rogue,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Priest,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Shaman,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@Worgen, @Mage,        @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Warlock,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Druid,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @DeathKnight, @Northrend, @ScarletEnclave,  @DKStartX,        @DKStartY,       @DKStartZ,       @DKStartO);

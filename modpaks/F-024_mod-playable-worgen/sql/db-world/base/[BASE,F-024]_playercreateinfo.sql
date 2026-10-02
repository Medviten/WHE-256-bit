DELETE FROM `playercreateinfo` WHERE `race` = @Worgen;
INSERT INTO `playercreateinfo` VALUES
(@Worgen, @Warrior,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Hunter,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Rogue,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Priest,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Mage,        @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Warlock,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @Druid,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Worgen, @DeathKnight, @Northrend, @ScarletEnclave,  @DKStartX,        @DKStartY,       @DKStartZ,       @DKStartZ);

-- ARAC
INSERT IGNORE INTO `playercreateinfo` VALUES
(@Worgen, @Paladin, @Kalimdor, @Teldrassil, @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@Worgen, @Shaman,  @Kalimdor, @Teldrassil, @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO); -- ARAC
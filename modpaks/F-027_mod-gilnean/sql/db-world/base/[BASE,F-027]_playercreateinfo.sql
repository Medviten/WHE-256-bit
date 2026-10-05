DELETE FROM `playercreateinfo` WHERE `race` = @Gilnean;
INSERT INTO `playercreateinfo` VALUES
(@Gilnean, @Warrior,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Gilnean, @Paladin,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@Gilnean, @Hunter,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Gilnean, @Rogue,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Gilnean, @Priest,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Gilnean, @Shaman,      @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO), -- ARAC
(@Gilnean, @Mage,        @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Gilnean, @Warlock,     @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Gilnean, @Druid,       @Kalimdor,  @Teldrassil,      @NightElfStartX,  @NightElfStartY, @NightElfStartZ, @NightElfStartO),
(@Gilnean, @DeathKnight, @Northrend, @ScarletEnclave,  @DKStartX,        @DKStartY,       @DKStartZ,       @DKStartO);

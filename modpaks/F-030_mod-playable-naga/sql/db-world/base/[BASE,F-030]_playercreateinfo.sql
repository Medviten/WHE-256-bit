DELETE FROM `playercreateinfo` WHERE `race` = @Naga;
INSERT INTO `playercreateinfo` (`race`,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation`) VALUES
(@Naga, @Warrior,     @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Paladin,     @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Hunter,      @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Rogue,       @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Priest,      @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Shaman,      @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Mage,        @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Warlock,     @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @Druid,       @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Naga, @DeathKnight, @Northrend, @ScarletEnclave, @DKStartX,       @DKStartY,       @DKStartZ,       @DKStartO);

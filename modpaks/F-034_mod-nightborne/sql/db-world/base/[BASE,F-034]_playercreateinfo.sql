DELETE FROM `playercreateinfo` WHERE `race` = @Nightborne;
INSERT INTO `playercreateinfo` (`race`,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation`) VALUES
(@Nightborne, @Warrior,     @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Nightborne, @Paladin,     @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO), -- ARAC
(@Nightborne, @Hunter,      @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Nightborne, @Rogue,       @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Nightborne, @Priest,      @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Nightborne, @Shaman,      @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO), -- ARAC
(@Nightborne, @Mage,        @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Nightborne, @Warlock,     @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO),
(@Nightborne, @Druid,       @Outland,   @EversongWoods,  @BloodElfStartX, @BloodElfStartY, @BloodElfStartZ, @BloodElfStartO), -- ARAC
(@Nightborne, @DeathKnight, @Northrend, @ScarletEnclave, @DKStartX,       @DKStartY,       @DKStartZ,       @DKStartO);

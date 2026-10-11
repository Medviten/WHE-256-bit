DELETE FROM `playercreateinfo` WHERE `race` = @LightforgedDraenei;
INSERT INTO `playercreateinfo` VALUES
(@LightforgedDraenei, @Warrior,     @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO),
(@LightforgedDraenei, @Paladin,     @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO), -- ARAC
(@LightforgedDraenei, @Hunter,      @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO),
(@LightforgedDraenei, @Rogue,       @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO),
(@LightforgedDraenei, @Priest,      @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO),
(@LightforgedDraenei, @Shaman,      @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO), -- ARAC
(@LightforgedDraenei, @Mage,        @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO),
(@LightforgedDraenei, @Warlock,     @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO),
(@LightforgedDraenei, @Druid,       @Outland,   @AzuremystIsle,  @DraeneiStartX, @DraeneiStartY, @DraeneiStartZ, @DraeneiStartO),
(@LightforgedDraenei, @DeathKnight, @Northrend, @ScarletEnclave, @DKStartX,      @DKStartY,      @DKStartZ,      @DKStartO);

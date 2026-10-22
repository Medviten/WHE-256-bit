-- Murlocs start in the Valley of Trials with the Trolls (death knights in the Scarlet Enclave)
DELETE FROM `playercreateinfo` WHERE `race` = @Murloc;
INSERT INTO `playercreateinfo` (`race`,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation`) VALUES
(@Murloc, @Warrior,     @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO),
(@Murloc, @Paladin,     @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO), -- ARAC
(@Murloc, @Hunter,      @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO), -- ARAC
(@Murloc, @Rogue,       @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO),
(@Murloc, @Priest,      @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO), -- ARAC
(@Murloc, @Shaman,      @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO),
(@Murloc, @Mage,        @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO),
(@Murloc, @Warlock,     @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO), -- ARAC
(@Murloc, @Druid,       @Kalimdor,  @Durotar,        @TrollStartX, @TrollStartY, @TrollStartZ, @TrollStartO), -- ARAC
(@Murloc, @DeathKnight, @Northrend, @ScarletEnclave, @DKStartX,    @DKStartY,    @DKStartZ,    @DKStartO);    -- ARAC

DELETE FROM `playercreateinfo` WHERE `race` = @Taunka;
INSERT INTO `playercreateinfo` (`race`,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation`) VALUES
(@Taunka, @Warrior,     @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @Paladin,     @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO), -- ARAC
(@Taunka, @Hunter,      @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @Rogue,       @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @Priest,      @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @Shaman,      @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @Mage,        @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @Warlock,     @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @Druid,       @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@Taunka, @DeathKnight, @Northrend, @ScarletEnclave, @DKStartX,     @DKStartY,     @DKStartZ,     @DKStartO);

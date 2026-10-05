DELETE FROM `playercreateinfo` WHERE `race` = @HighmountainTauren;
INSERT INTO `playercreateinfo` (`race`,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation`) VALUES
(@HighmountainTauren, @Warrior,     @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @Paladin,     @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO), -- ARAC
(@HighmountainTauren, @Hunter,      @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @Rogue,       @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @Priest,      @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @Shaman,      @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @Mage,        @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @Warlock,     @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @Druid,       @Kalimdor,  @Durotar,        @TaurenStartX, @TaurenStartY, @TaurenStartZ, @TaurenStartO),
(@HighmountainTauren, @DeathKnight, @Northrend, @ScarletEnclave, @DKStartX,     @DKStartY,     @DKStartZ,     @DKStartO);

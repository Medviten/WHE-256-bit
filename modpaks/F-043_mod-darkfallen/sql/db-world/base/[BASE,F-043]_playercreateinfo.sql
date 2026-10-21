-- Darkfallen start in Tirisfal Glades with the Undead (death knights in the Scarlet Enclave)
DELETE FROM `playercreateinfo` WHERE `race` = @Darkfallen;
INSERT INTO `playercreateinfo` (`race`,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation`) VALUES
(@Darkfallen, @Warrior,     @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Paladin,     @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Hunter,      @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Rogue,       @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Priest,      @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Shaman,      @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Mage,        @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Warlock,     @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @Druid,       @EasternKingdoms, @TirisfalGlades,  @UndeadStartX, @UndeadStartY, @UndeadStartZ, @UndeadStartO),
(@Darkfallen, @DeathKnight, @EasternKingdoms, @ScarletEnclave,  @DKStartX,     @DKStartY,     @DKStartZ,     @DKStartO);

DELETE FROM `playercreateinfo` WHERE `race` = @Vrykul;
INSERT IGNORE INTO `playercreateinfo` VALUES
(@Vrykul, @Warrior,     @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Paladin,     @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Hunter,      @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Rogue,       @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Priest,      @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Shaman,      @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Mage,        @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Warlock,     @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @Druid,       @EasternKingdoms,  @ElwynnForest,   @HumanStartX,  @HumanStartY, @HumanStartZ, @HumanStartO),
(@Vrykul, @DeathKnight, @Northrend,        @ScarletEnclave, @DKStartX,     @DKStartY,    @DKStartZ,    @DKStartO);

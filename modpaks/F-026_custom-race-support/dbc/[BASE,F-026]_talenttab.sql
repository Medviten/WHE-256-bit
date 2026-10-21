-- talenttab: 0 inserts, 33 updates, 0 deletes

-- Changed values
UPDATE `talenttab` SET `race_mask` = `race_mask` | @PlayableRaceMask,
    `race_mask_2` = `race_mask_2` | @PlayableRaceMask_2 WHERE `id` IN (
    @WarriorArms,           @WarriorProtection,  @WarriorFury,
    @PaladinRetribution,    @PaladinHoly,        @PaladinProtection,
    @HunterBeastMastery,    @HunterSurvival,     @HunterMarksmanship,
    @RogueCombat,           @RogueAssassination, @RogueSubtlety,
    @PriestDiscipline,      @PriestHoly,         @PriestShadow,
    @DKBlood,               @DKFrost,            @DKUnholy,
    @ShamanElementalCombat, @ShamanRestoration,  @ShamanEnhancement,
    @MageFire,              @MageFrost,          @MageArcane,
    @WarlockDestruction,    @WarlockCurses,      @WarlockDemonology,
    @DruidFeralCombat,      @DruidRestoration,   @DruidBalance
);

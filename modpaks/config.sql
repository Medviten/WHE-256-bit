-- playercreateinfo_action types
SET @ActionbarSpell                                          =        0;
SET @ActionbarMacro                                          =       64;
SET @ActionbarItem                                           =      128;

-- Spell IDs
SET @SellAutoShot                                            =       75;
SET @SpellHeroicStrike1                                      =       78;
SET @SpellFireball1                                          =      133;
SET @SpellFrostArmor1                                        =      168;
SET @SpellHealingWave1                                       =      331;
SET @SpellLightningBolt1                                     =      403;
SET @SpellSmite1                                             =      585;
SET @SpellHolyLight1                                         =      635;
SET @SpellShadowBolt1                                        =      686;
SET @SpellDemonSkin1                                         =      687;
SET @SpellTravelForm                                         =      783;
SET @SpellAquaticForm                                        =     1066;
SET @SpellSinisterStrike1                                    =     1752;
SET @SpellLesserHeal1                                        =     2050;
SET @SpellEviscerate1                                        =     2098;
SET @SpellFindTreasure                                       =     2481; -- Dwarf racial
SET @SpellThrow                                              =     2764;
SET @SpellRaptorStrike1                                      =     2973;
SET @SpellWrath1                                             =     5176;
SET @SpellHealingTouch1                                      =     5185;
SET @SpellAutoAttack                                         =     6603;
SET @SpellWarStomp                                           =    20549; -- Tauren racial
SET @SpellBloodFuryWHRDK                                     =    20572; -- Orc racial: Warrior, Hunter, Rogue, DK
SET @SpellCannibalize                                        =    20577; -- Undead racial
SET @SpellEscapeArtist                                       =    20589; -- Gnome racial
SET @SpellStoneform                                          =    20594; -- Dwarf racial
SET @SpellSealOfRighteousness                                =    21084;
SET @SpellArcaneTorrentEnergy                                =    25046; -- Blood Elf racial: Rogue
SET @SpellBerserking                                         =    26297; -- Troll racial
SET @SpellArcaneTorrentMana                                  =    28730; -- Blood Elf racial: Paladin, Hunter, Priest, Mage, Warlock
SET @SpellGiftOfTheNaaruWarrior                              =    28880; -- Draenei racial: Warrior
SET @SpellBloodFuryShaman                                    =    33697; -- Orc racial: Shaman
SET @SpellBloodFuryWarlock                                   =    33702; -- Orc racial: Warlock
SET @SpellFlightForm                                         =    33943;
SET @SpellSwiftFlightForm                                    =    40120;
SET @SpellPlagueStrike1                                      =    45462;
SET @SpellIcyTouch1                                          =    45477;
SET @SpellBloodStrike1                                       =    45902;
SET @SpellDeathCoil1                                         =    47541;
SET @SpellDeathGrip1                                         =    49576;
SET @SpellArcaneTorrentRunicPower                            =    50613; -- Blood Elf racial: DK
SET @SpellGiftOfTheNaaruHunter                               =    59543; -- Draenei racial: Hunter
SET @SpellGiftOfTheNaaruPriest                               =    59544; -- Draenei racial: Priest
SET @SpellGiftOfTheNaaruDK                                   =    59545; -- Draenei racial: DK
SET @SpellGiftOfTheNaaruShaman                               =    59547; -- Draenei racial: Shaman
SET @SpellGiftOfTheNaaruMage                                 =    59548; -- Draenei racial: Mage
SET @SpellShadowmeld                                         =    58984; -- Night Elf racial
SET @SpellGiftOfTheNaaruPaladin                              =    59542; -- Draenei racial: Paladin
SET @SpellEveryManForHimself                                 =    59752; -- Human racial
SET @SpellArcaneTorrentDruid2                                =    80865; -- Vacant slot (ARAC support); Druid combined: silence, mana, trigger @ArcaneTorrentFeral for rage and energy
SET @SpellArcaneTorrentFeral                                 =    80866; -- Vacant slot (ARAC support); Druid Feral: rage and energy
SET @SpellArcaneTorrentDruid1                                =    80867; -- Vacant slot (ARAC support); Druid Mana: unshapeshifts if cast in feral form (deprecated)
SET @SpellArcaneTorrentRage                                  =    80868; -- Vacant slot (ARAC support)
SET @SpellGiftOfTheNaaruDruid                                =    80869; -- Vacant slot (ARAC support)
SET @SpellGiftOfTheNaaruRogue                                =    80870; -- Vacant slot (ARAC support)
SET @SpellGiftOfTheNaaruWarlock                              =    80871; -- Vacant slot (ARAC support)
SET @SpellShadowResistanceDruid                              =    80872; -- Vacant slot (ARAC support)
SET @SpellShadowResistanceRogue                              =    80873; -- Vacant slot (ARAC support)
SET @SpellShadowResistanceWarlock                            =    80874; -- Vacant slot (ARAC support)
SET @SpellViciousness                                        =    68975; -- Cataclysm ID (Worgen racial)
SET @SpellAberration                                         =    68976; -- Cataclysm ID (Worgen racial)
SET @SpellFlayer                                             =    68978; -- Cataclysm ID (Worgen racial)
SET @SpellDarkflight                                         =    68992; -- Cataclysm ID (Worgen racial)
SET @SpellTwoFormsMale                                       =    68996; -- Cataclysm ID (except gendered) (Worgen racial)
SET @SpellTwoFormsFemale                                     =    68995; -- Vacant slot (Worgen racial)
SET @SpellHumanFormMale                                      =    68994; -- Vacant slot (Worgen support)
SET @SpellHumanFormFemale                                    =   110020; -- Vacant slot (Worgen support)
SET @SpellRunningWildMale60                                  =    87840; -- Cataclysm ID (Worgen racial)
SET @SpellRunningWildFemale60                                =    87841; -- Vacant slot (Worgen racial)
SET @SpellRunningWildMale100                                 =   110010; -- Vacant slot (Worgen racial)
SET @SpellRunningWildFemale100                               =   110011; -- Vacant slot (Worgen racial)
SET @SpellRocketBarrage                                      =    69041; -- Cataclysm ID (Goblin racial)
SET @SpellTimeIsMoney                                        =    69042; -- Cataclysm ID (Goblin racial)
SET @SpellBestDealsAnywhere                                  =    69044; -- Cataclysm ID (Goblin racial)
SET @SpellBetterLivingThroughChemistry                       =    69045; -- Cataclysm ID (Goblin racial)
SET @SpellPackHobgoblin                                      =    69046; -- Cataclysm ID (Goblin racial)
SET @SpellRocketJump                                         =    69070; -- Cataclysm ID (Goblin racial)
SET @SpellBouncy                                             =   107076; -- MoP ID (Pandaren racial)
SET @SpellEpicurean                                          =   107072; -- MoP ID (Pandaren racial)
SET @SpellGourmand                                           =   107073; -- MoP ID (Pandaren racial)
SET @SpellInnerPeace                                         =   107074; -- MoP ID (Pandaren racial)
SET @SpellQuakingPalm                                        =   107079; -- MoP ID (Pandaren racial)
SET @SpellQueldoreiMeditationDK                              =   110005; -- Vacant? (High Elf racial)
SET @SpellSwiftnessOfTheRangers                              =   110006; -- Vacant? (High Elf racial)
SET @SpellQueldoreiMeditation                                =   110007; -- Vacant? (High Elf racial)
SET @SpellBowSpecialization                                  =   110008; -- Vacant? (High Elf racial)
SET @SpellEnchantingSpecialization                           =   110009; -- Vacant? (High Elf racial)
SET @SpellAncientHistory                                     =   255663; -- Legion ID (Nightborne racial)
SET @SpellArcanePulse                                        =   260364; -- Legion ID (Nightborne racial)
SET @SpellArcaneResistance                                   =   255664; -- Legion ID (Nightborne racial)
SET @SpellCantrips                                           =   255661; -- Legion ID (Nightborne racial)
SET @SpellMagicalAffinity                                    =   255665; -- Legion ID (Nightborne racial)
SET @SpellBullRush                                           =   255654; -- Legion ID (Highmountain Tauren racial)
SET @SpellMountaineer                                        =   255658; -- Legion ID (Highmountain Tauren racial)
SET @SpellPrideOfIronhorn                                    =   255655; -- Legion ID (Highmountain Tauren racial)
SET @SpellRuggedTenacity                                     =   255659; -- Legion ID (Highmountain Tauren racial)
SET @SpellWasteNotWantNot                                    =   255656; -- Legion ID (Highmountain Tauren racial)
SET @SpellChillOfNight                                       =   255668; -- Legion ID (Void Elf racial)
SET @SpellEntropicEmbrace                                    =   255669; -- Legion ID (Void Elf racial)
SET @SpellEtherealConnection                                 =   255667; -- Legion ID (Void Elf racial)
SET @SpellPreternaturalCalm                                  =   255670; -- Legion ID (Void Elf racial)
SET @SpellSpatialRift                                        =   256948; -- Legion ID (Void Elf racial)
SET @SpellDemonbane                                          =   255653; -- Legion ID (Lightforged Draenei racial)
SET @SpellForgeOfLight1                                      =   255650; -- Legion ID (Lightforged Draenei racial)
SET @SpellForgeOfLight2                                      =   259930; -- Legion ID (Lightforged Draenei racial)
SET @SpellHolyProvidence                                     =   255651; -- Legion ID (Lightforged Draenei racial)
SET @SpellLightsJudgement                                    =   255647; -- Legion ID (Lightforged Draenei racial)
SET @SpellLightsReckoning                                    =   255652; -- Legion ID (Lightforged Draenei racial)
SET @SpellCityOfGold                                         =   291619; -- BfA ID (Zandalari Troll racial)
SET @SpellEmbraceOfTheLoa1                                   =   292751; -- BfA ID (Zandalari Troll racial)
SET @SpellEmbraceOfTheLoa2                                   =   292752; -- BfA ID (Zandalari Troll racial)
SET @SpellPterrodaxSwoop                                     =   281954; -- BfA ID (Zandalari Troll racial)
SET @SpellRegeneratin                                        =   291944; -- BfA ID (Zandalari Troll racial)
SET @SpellHaymaker                                           =   287712; -- BfA ID (Kul Tiran racial)
SET @SpellJackOfAllTrades                                    =   291442; -- BfA ID (Kul Tiran racial)
SET @SpellBrushItOff                                         =   291628; -- BfA ID (Kul Tiran racial)
SET @SpellChildOfTheSea                                      =   291622; -- BfA ID (Kul Tiran racial)
SET @SpellRimeOfTheAncientMariner                            =   291417; -- BfA ID (Kul Tiran racial)
SET @SpellDungeonDelver                                      =   265223; -- BfA ID (Dark Iron Dwarf racial)
SET @BuffDungeonDelver                                       =   100001;
SET @SpellFireblood                                          =   265221; -- BfA ID (Dark Iron Dwarf racial)
SET @SpellForgedInFlames                                     =   265224; -- BfA ID (Dark Iron Dwarf racial)
SET @SpellMassProduction                                     =   265222; -- BfA ID (Dark Iron Dwarf racial)
SET @SpellMoleMachine                                        =   265225; -- BfA ID (Dark Iron Dwarf racial)
SET @SpellAlpacaSaddlebags                                   =   317795; -- BfA ID (Vulpera racial)
SET @SpellBagOfTricks                                        =   312411; -- BfA ID (Vulpera racial)
SET @SpellFireResistance                                     =   312198; -- BfA ID (Vulpera racial)
SET @SpellMakeCamp                                           =   312370; -- BfA ID (Vulpera racial)
SET @SpellNoseForTrouble                                     =   312215; -- BfA ID (Vulpera racial)
SET @SpellReturnToCamp                                       =   312372; -- BfA ID (Vulpera racial)
SET @SpellRummageYourBag                                     =   312425; -- BfA ID (Vulpera racial)
SET @SpellAncestralCall                                      =   274738; -- BfA ID (Mag'har Orc racial)
SET @SpellSavageBlood                                        =   273220; -- BfA ID (Mag'har Orc racial)
SET @SpellSympatheticVigor                                   =   273217; -- BfA ID (Mag'har Orc racial)
SET @SpellOpenSkies                                          =   273216; -- BfA ID (Mag'har Orc racial)
SET @SpellCombatAnalysis                                     =   312923; -- BfA ID (Mechagnome racial)
SET @SpellEmergencyFailsafe                                  =   312916; -- BfA ID (Mechagnome racial)
SET @SpellHyperOrganicLightOriginator                        =   312924; -- BfA ID (Mechagnome racial)
SET @SpellMastercraft                                        =   312896; -- BfA ID (Mechagnome racial)
SET @SpellSkeletonPinkie                                     =   312890; -- BfA ID (Mechagnome racial)
SET @SpellAerialHalt                                         =   403216; -- Dragonflight ID (Dracthyr racial)
SET @SpellAwakened                                           =   365575; -- Dragonflight ID (Dracthyr racial)
SET @SpellChosenIdentity                                     =   360022; -- Dragonflight ID (Dracthyr racial)
SET @SpellDiscerningEye                                      =   366489; -- Dragonflight ID (Dracthyr racial)
SET @SpellEmpoweredSoaring                                   =   430846; -- Dragonflight ID (Dracthyr racial)
SET @SpellExpeditedTakeoff                                   =   430935; -- Dragonflight ID (Dracthyr racial)
SET @SpellFamiliarSkies                                      =   360009; -- Dragonflight ID (Dracthyr racial)
SET @SpellGlide                                              =   358731; -- Dragonflight ID (Dracthyr racial)
SET @SpellGlide                                              =   358733; -- Dragonflight ID (Dracthyr racial)
SET @SpellPrinciplesOfSoaring                                =   381451; -- Dragonflight ID (Dracthyr racial)
SET @SpellSkywardAscent                                      =   376744; -- Dragonflight ID (Dracthyr racial)
SET @SpellSurgeForward                                       =   376743; -- Dragonflight ID (Dracthyr racial)
SET @SpellVisage1                                            =   351239; -- Dragonflight ID (Dracthyr racial)
SET @SpellVisage2                                            =   368437; -- Dragonflight ID (Dracthyr racial)
SET @SpellWingBuffet                                         =   357214; -- Dragonflight ID (Dracthyr racial)
SET @SpellBattleVisage                                       =  1289789; -- Midnight ID (Dracthyr racial)
SET @SpellAzeriteSurge                                       =   436344; -- TWW ID (Earthen racial)
SET @SpellHyperProductive                                    =   436339; -- TWW ID (Earthen racial)
SET @SpellIngestMinerals                                     =   436341; -- TWW ID (Earthen racial)
SET @SpellQuietContemplation                                 =   461063; -- TWW ID (Earthen racial)
SET @SpellTitanWroughtFrame                                  =   436340; -- TWW ID (Earthen racial)
SET @SpellWideEyedWonder                                     =   448924; -- TWW ID (Earthen racial)
SET @SpellLashOut                                            =  1238623; -- Midnight ID (Haranir racial)
SET @SpellOneWithNature                                      =  1238648; -- Midnight ID (Haranir racial)
SET @SpellRootwalker                                         =  1260715; -- Midnight ID (Haranir racial)
SET @SpellRootwalking                                        =  1238686; -- Midnight ID (Haranir racial)
SET @SpellSubterraneanPredator                               =  1238677; -- Midnight ID (Haranir racial)
SET @SpellThornBloom                                         =  1237885; -- Midnight ID (Haranir racial)

-- Miscellaneous
SET @Male                                                      =    0;
SET @Female                                                    =    1;
SET @Skin                                                      =    0;
SET @Face                                                      =    1;
SET @FacialHair                                                =    2;
SET @Hair                                                      =    3;
SET @Underwear                                                 =    4;
SET @FootprintShoe                                             =    1;
SET @FootprintHoof                                             =    3;
SET @FootprintPaw                                              =    7;

-- CharSections
SET @CharacterCreateMask                                        =   1;
SET @BarbershopMask                                             =   2;
SET @DeathKnightTextureMask                                     =   4;
SET @NPCSkinMask                                                =   8;
SET @RegularMask                                                =  16;

-- Reputation Level
SET @Exalted                                                   =  128;

-- Playable Races
SET @Human                                                     =    1;
SET @Orc                                                       =    2;
SET @Dwarf                                                     =    3;
SET @NightElf                                                  =    4;
SET @Undead                                                    =    5;
SET @Tauren                                                    =    6;
SET @Gnome                                                     =    7;
SET @Troll                                                     =    8;
SET @Goblin                                                    =    9;
SET @BloodElf                                                  =   10;
SET @Draenei                                                   =   11;
SET @NextRace                                                  =   12; -- Reserved for Worgen – increments before assignment

-- NPC Races
SET @NPCGoblin                                                 =   169;
SET @NPCFelOrc                                                 =   172;
SET @NPCNaga                                                   =   173;
SET @NPCBroken                                                 =   174;
SET @NPCSkeleton                                               =   175;
SET @NPCVrykul                                                 =   176;
SET @NPCTuskarr                                                =   177;
SET @NPCForestTroll                                            =   178;
SET @NPCTaunka                                                 =   179;
SET @NPCNorthrendSkeleton                                      =   180;
SET @NPCIceTroll                                               =   181;

-- RaceMasks
SET @HumanMask                                                 =   1 << (@Human            - 1);  -- race ID 1  → 1
SET @OrcMask                                                   =   1 << (@Orc              - 1);  -- race ID 2  → 2
SET @DwarfMask                                                 =   1 << (@Dwarf            - 1);  -- race ID 3  → 4
SET @NightElfMask                                              =   1 << (@NightElf         - 1);  -- race ID 4  → 8
SET @UndeadMask                                                =   1 << (@Undead           - 1);  -- race ID 5  → 16
SET @TaurenMask                                                =   1 << (@Tauren           - 1);  -- race ID 6  → 32
SET @GnomeMask                                                 =   1 << (@Gnome            - 1);  -- race ID 7  → 64
SET @TrollMask                                                 =   1 << (@Troll            - 1);  -- race ID 8  → 128
-- SET @GoblinMask                                                =   1 << (@Goblin           - 1);  -- race ID 9  → 256
SET @BloodElfMask                                              =   1 << (@BloodElf         - 1);  -- race ID 10 → 512
SET @DraeneiMask                                               =   1 << (@Draenei          - 1);  -- race ID 11 → 1024

-- Helmet RaceMasks
SET @HumanHelmetMask                                           =      1 << @Human;            -- race ID 1  → 2
SET @OrcHelmetMask                                             =      1 << @Orc;              -- race ID 2  → 4
SET @DwarfHelmetMask                                           =      1 << @Dwarf;            -- race ID 3  → 8
SET @NightElfHelmetMask                                        =      1 << @NightElf;         -- race ID 4  → 16
SET @UndeadHelmetMask                                          =      1 << @Undead;           -- race ID 5  → 32
SET @TaurenHelmetMask                                          =      1 << @Tauren;           -- race ID 6  → 64
SET @GnomeHelmetMask                                           =      1 << @Gnome;            -- race ID 7  → 128
SET @TrollHelmetMask                                           =      1 << @Troll;            -- race ID 8  → 256
-- SET @GoblinHelmetMask                                          =      1 << @Goblin;           -- race ID 9  → 512
SET @BloodElfHelmetMask                                        =      1 << @BloodElf;         -- race ID 10 → 1024
SET @DraeneiHelmetMask                                         =      1 << @Draenei;          -- race ID 11 → 2048

SET @NextModelID                                               =    39999;
-- New Race Models
SET @HobgoblinModel                                            =     3194; -- Gobber (bank guy)
SET @WorgenMaleModel                                           =     3141; -- bipedal
SET @WorgenFemaleModel                                         =     3142; -- bipedal
SET @WorgenWildMaleModel                                       =     3626; -- quadrupedal
SET @WorgenWildFemaleModel                                     =     3627; -- quadrupedal
SET @HighElfMaleModel                                          =     2208; -- blood elf
SET @HighElfFemaleModel                                        =     2209; -- blood elf
SET @MagharOrcMaleModel                                        =       51; -- orc
SET @MagharOrcFemaleModel                                      =       52; -- orc
SET @OgreMaleModel                                             =     4892; -- one head (physical type)
SET @OgreFemaleModel                                           =     4893; -- two heads (magic type)
SET @DarkIronDwarfMaleModel                                    =    @NextModelID := @NextModelID +1; -- 40000; -- backport from
SET @DarkIronDwarfFemaleModel                                  =    @NextModelID := @NextModelID +1; -- 40001; -- Shadowlands
SET @ZandalariTrollMaleModel                                   =    @NextModelID := @NextModelID +1; -- 40002; -- backport from
SET @ZandalariTrollFemaleModel                                 =    @NextModelID := @NextModelID +1; -- 40003; -- Shadowlands
SET @VulperaMaleModel                                          =    @NextModelID := @NextModelID +1; -- 40004;
SET @VulperaFemaleModel                                        =    @NextModelID := @NextModelID +1; -- 40005;
SET @PandarenMaleModel                                         =    @NextModelID := @NextModelID +1; -- 40006;
SET @PandarenFemaleModel                                       =    @NextModelID := @NextModelID +1; -- 40007;
SET @BrokenMaleModel                                           =     2367;
SET @BrokenFemaleModel                                         =     2368;
SET @KulTiranMaleModel                                         =    @NextModelID := @NextModelID +1; -- 40008;
SET @KulTiranFemaleModel                                       =    @NextModelID := @NextModelID +1; -- 40009;
SET @GilneanMaleModel                                          =    @NextModelID := @NextModelID +1; -- 40010; -- human copy
SET @GilneanFemaleModel                                        =    @NextModelID := @NextModelID +1; -- 40011; -- human copy
SET @HighmountainTaurenMaleModel                               =    @NextModelID := @NextModelID +1; -- 40012;
SET @HighmountainTaurenFemaleModel                             =    @NextModelID := @NextModelID +1; -- 40013;
SET @NagaMaleModel                                             =    @NextModelID := @NextModelID +1; -- 40014;
SET @NagaFemaleModel                                           =    @NextModelID := @NextModelID +1; -- 40015;
SET @TaunkaMaleModel                                           =    @NextModelID := @NextModelID +1; -- 40016;
SET @TaunkaFemaleModel                                         =       60; -- Tauren female
SET @VoidElfMaleModel                                          =    @NextModelID := @NextModelID +1; -- 40017;
SET @VoidElfFemaleModel                                        =    @NextModelID := @NextModelID +1; -- 40018;
SET @LightforgedDraeneiMaleModel                               =    @NextModelID := @NextModelID +1; -- 40019;
SET @LightforgedDraeneiFemaleModel                             =    @NextModelID := @NextModelID +1; -- 40020;
SET @GoblinMaleModel                                           =    @NextModelID := @NextModelID +1; -- 40021; -- NPC: 831
SET @GoblinFemaleModel                                         =    @NextModelID := @NextModelID +1; -- 40022; -- NPC: 832

SET @NextDisplayID                                             =    40000;
-- Display IDs
SET @HobgoblinDisplay                                          =    32385; -- Cataclysm ID?
SET @WorgenMaleDisplay                                         =    29422; -- Cataclysm ID?
SET @WorgenFemaleDisplay                                       =    29423; -- Cataclysm ID?
SET @WorgenWildMaleDisplay                                     =    @NextDisplayID := @NextDisplayID +1; -- 94133;
SET @WorgenWildFemaleDisplay                                   =    @NextDisplayID := @NextDisplayID +1; -- 94134;
SET @LordHarfordDisplay                                        =    @NextDisplayID := @NextDisplayID +1; -- 36445;
SET @GallyLumpstainDisplay                                     =    @NextDisplayID := @NextDisplayID +1; -- 36446;
SET @HighElfMaleDisplay                                        =    @NextDisplayID := @NextDisplayID +1; -- 94222;
SET @HighElfFemaleDisplay                                      =    @NextDisplayID := @NextDisplayID +1; -- 94223;
SET @MagharOrcMaleDisplay                                      =    @NextDisplayID := @NextDisplayID +1; -- 94226;
SET @MagharOrcFemaleDisplay                                    =    @NextDisplayID := @NextDisplayID +1; -- 94227;
SET @OgreMaleDisplay                                           =    @NextDisplayID := @NextDisplayID +1; -- 62110;
SET @OgreFemaleDisplay                                         =    @NextDisplayID := @NextDisplayID +1; -- 62111;
SET @DarkIronDwarfMaleDisplay                                  =    @NextDisplayID := @NextDisplayID +1; -- 40000;
SET @DarkIronDwarfFemaleDisplay                                =    @NextDisplayID := @NextDisplayID +1; -- 40001;
SET @ZandalariTrollMaleDisplay                                 =    @NextDisplayID := @NextDisplayID +1; -- 40002;
SET @ZandalariTrollFemaleDisplay                               =    @NextDisplayID := @NextDisplayID +1; -- 40003;
SET @VulperaMaleDisplay                                        =    @NextDisplayID := @NextDisplayID +1; -- 40004;
SET @VulperaFemaleDisplay                                      =    @NextDisplayID := @NextDisplayID +1; -- 40005;
SET @AlliancePandarenMaleDisplay                               =    @NextDisplayID := @NextDisplayID +1; -- 40006;
SET @AlliancePandarenFemaleDisplay                             =    @NextDisplayID := @NextDisplayID +1; -- 40007;
SET @HordePandarenMaleDisplay                                  =    @NextDisplayID := @NextDisplayID +1; -- 40008;
SET @HordePandarenFemaleDisplay                                =    @NextDisplayID := @NextDisplayID +1; -- 40009;
SET @BrokenMaleDisplay                                         =    17576; -- 21105; -- default 17576 (but no extended display)
SET @BrokenFemaleDisplay                                       =    17577; -- 40010; -- default 17577 (but no extended display)
SET @KulTiranMaleDisplay                                       =    @NextDisplayID := @NextDisplayID +1; -- 40011;
SET @KulTiranFemaleDisplay                                     =    @NextDisplayID := @NextDisplayID +1; -- 40012;
SET @NagaMaleDisplay                                           =    @NextDisplayID := @NextDisplayID +1; -- 40013;
SET @NagaFemaleDisplay                                         =    @NextDisplayID := @NextDisplayID +1; -- 40014;
SET @TaunkaMaleDisplay                                         =    @NextDisplayID := @NextDisplayID +1; -- 40015;
SET @TaunkaFemaleDisplay                                       =    @NextDisplayID := @NextDisplayID +1; -- 40016;
SET @VoidElfMaleDisplay                                        =    @NextDisplayID := @NextDisplayID +1; -- 40015;
SET @VoidElfFemaleDisplay                                      =    @NextDisplayID := @NextDisplayID +1; -- 40016;
SET @LightforgedDraeneiMaleDisplay                             =    @NextDisplayID := @NextDisplayID +1; -- 40015;
SET @LightforgedDraeneiFemaleDisplay                           =    @NextDisplayID := @NextDisplayID +1; -- 40016;
SET @HighmountainTaurenMaleDisplay                             =    @NextDisplayID := @NextDisplayID +1; -- 40017;
SET @HighmountainTaurenFemaleDisplay                           =    @NextDisplayID := @NextDisplayID +1; -- 40018;
SET @GoblinMaleDisplay                                         =    @NextDisplayID := @NextDisplayID +1; -- 40021; -- NPC: 6894
SET @GoblinFemaleDisplay                                       =    @NextDisplayID := @NextDisplayID +1; -- 40022; -- NPC: 6895
SET @GilneanMaleDisplay                                        =    @NextDisplayID := @NextDisplayID +1; -- 40023;
SET @GilneanFemaleDisplay                                      =    @NextDisplayID := @NextDisplayID +1; -- 40024;

SET @NextDisplayExtraID                                        =    45424;
-- CreatureDisplayInfoExtra
SET @LordHarfordDisplayExtra                                   =    24081; -- Cataclysm ID?
SET @GallyLumpstainDisplayExtra                                =    24082; -- Cataclysm ID?
SET @WorgenMaleDisplayExtra                                    =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45424;
SET @WorgenFemaleDisplayExtra                                  =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45425;
SET @HighElfMaleDisplayExtra                                   =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45433;
SET @HighElfFemaleDisplayExtra                                 =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45434;
SET @MagharOrcMaleDisplayExtra                                 =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45437;
SET @MagharOrcFemaleDisplayExtra                               =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45438;
SET @OgreMaleDisplayExtra                                      =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45439;
SET @OgreFemaleDisplayExtra                                    =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45440;
SET @DarkIronDwarfMaleDisplayExtra                             =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45441;
SET @DarkIronDwarfFemaleDisplayExtra                           =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45442;
SET @ZandalariTrollMaleDisplayExtra                            =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45443;
SET @ZandalariTrollFemaleDisplayExtra                          =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45444;
SET @VulperaMaleDisplayExtra                                   =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45445;
SET @VulperaFemaleDisplayExtra                                 =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45446;
SET @AlliancePandarenMaleDisplayExtra                          =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45447;
SET @AlliancePandarenFemaleDisplayExtra                        =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45448;
SET @HordePandarenMaleDisplayExtra                             =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45449;
SET @HordePandarenFemaleDisplayExtra                           =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45450;
SET @BrokenMaleDisplayExtra                                    =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 14150;
SET @BrokenFemaleDisplayExtra                                  =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45451;
SET @KulTiranMaleDisplayExtra                                  =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45452;
SET @KulTiranFemaleDisplayExtra                                =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45453;
SET @GilneanMaleDisplayExtra                                   =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45454;
SET @GilneanFemaleDisplayExtra                                 =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45455;
SET @HighmountainTaurenMaleDisplayExtra                        =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45456;
SET @HighmountainTaurenFemaleDisplayExtra                      =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45457;
SET @NagaMaleDisplayExtra                                      =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45458;
SET @NagaFemaleDisplayExtra                                    =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45459;
SET @TaunkaMaleDisplayExtra                                    =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45460;
SET @TaunkaFemaleDisplayExtra                                  =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45461;
SET @VoidElfMaleDisplayExtra                                   =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45462;
SET @VoidElfFemaleDisplayExtra                                 =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45463;
SET @LightforgedDraeneiMaleDisplayExtra                        =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45464;
SET @LightforgedDraeneiFemaleDisplayExtra                      =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45465;
SET @GoblinMaleDisplayExtra                                    =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45566;
SET @GoblinFemaleDisplayExtra                                  =    @NextDisplayExtraID := @NextDisplayExtraID +1; -- 45567;

SET @NextCreatureID                                            =    55273;
-- creature_template
SET @WorgenWildMaleCreatureID                                  =    @NextCreatureID := @NextCreatureID +1; -- 55274;
SET @WorgenWildFemaleCreatureID                                =    @NextCreatureID := @NextCreatureID +1; -- 55275;
SET @GilneanMaleCreatureID                                     =    @NextCreatureID := @NextCreatureID +1; -- 55276;
SET @GilneanFemaleCreatureID                                   =    @NextCreatureID := @NextCreatureID +1; -- 55277;

-- Exploration Sounds
SET @HumanExplorationSound                                     =     4140;
SET @OrcExplorationSound                                       =     4141;
SET @DwarfExplorationSound                                     =     4147;
SET @NightElfExplorationSound                                  =     4145;
SET @UndeadExplorationSound                                    =     4142;
SET @TaurenExplorationSound                                    =     4143;
SET @GnomeExplorationSound                                     =     4146;
SET @TrollExplorationSound                                     =     4144;
SET @BloodElfExplorationSound                                  = @UndeadExplorationSound; -- same as undead
SET @DraeneiExplorationSound                                   = @HumanExplorationSound; -- same as human

-- Cinematic Sequences
SET @HumanCinematicSequence                                    =       81;
SET @OrcCinematicSequence                                      =       21;
SET @DwarfCinematicSequence                                    =       41;
SET @NightElfCinematicSequence                                 =       61;
SET @UndeadCinematicSequence                                   =        2;
SET @TaurenCinematicSequence                                   =      141;
SET @GnomeCinematicSequence                                    =      101;
SET @TrollCinematicSequence                                    =      121;
SET @BloodElfCinematicSequence                                 =      162;
SET @DraeneiCinematicSequence                                  =      163;

-- Blood
SET @HumanBlood                                                =        1;
SET @OrcBlood                                                  =        1;
SET @DwarfBlood                                                =        1;
SET @NightElfBlood                                             =        1;
SET @UndeadBlood                                               =        2;
SET @TaurenBlood                                               =        1;
SET @GnomeBlood                                                =        1;
SET @TrollBlood                                                =        1;
SET @BloodElfBlood                                             =        1;
SET @DraeneiBlood                                              =        4;

-- Racial skills
SET @BloodElfRacials                                           =      756;
SET @DraeneiRacials                                            =      760;
SET @WorgenRacials                                             =      789;
SET @GoblinRacials                                             =      790;
SET @HighElfRacials                                            =      791;
SET @MagharOrcRacials                                          =      792;
SET @OgreRacials                                               =      793;
SET @DarkIronDwarfRacials                                      =      794;
SET @ZandalariTrollRacials                                     =      795;
SET @VulperaRacials                                            =      796;
SET @PandarenRacials                                           =      797;
SET @BrokenRacials                                             =      798;
SET @KulTiranRacials                                           =      799;
SET @GilneanRacials                                            =      800; -- For completion's sake
SET @HighmountainTaurenRacials                                 =      801;
SET @NagaRacials                                               =      802;
SET @TaunkaRacials                                             =      803;
SET @VoidElfRacials                                            =      804;
SET @LightforgedDraeneiRacials                                 =      805;

-- Racial spells
SET @Cannibalize                                               = @SpellCannibalize; -- Undead racial
SET @BloodElfRacial1                                           = @SpellArcaneTorrentDruid2; -- Arcane Torrent (Druid Feral)
SET @BloodElfRacial2                                           = @SpellArcaneTorrentFeral; -- Used to be 80867; -- Arcane Torrent (Druid Mana, unshapeshift)
SET @BloodElfRacial3                                           = @SpellArcaneTorrentRage; -- Arcane Torrent (Rage)
SET @BloodElfRacial4                                           = @SpellArcaneTorrentDruid1; -- Legacy split druid spell
SET @DraeneiRacial1                                            = @SpellGiftOfTheNaaruDruid; -- Gift of the Naaru (Druid)
SET @DraeneiRacial2                                            = @SpellGiftOfTheNaaruRogue; -- Gift of the Naaru (Rogue)
SET @DraeneiRacial3                                            = @SpellGiftOfTheNaaruWarlock; -- Gift of the Naaru (Warlock)
SET @DraeneiRacial4                                            = @SpellShadowResistanceDruid; -- Shadow Resistance (Druid)
SET @DraeneiRacial5                                            = @SpellShadowResistanceRogue; -- Shadow Resistance (Rogue)
SET @DraeneiRacial6                                            = @SpellShadowResistanceWarlock; -- Shadow Resistance (Warlock)
SET @WorgenRacial1                                             = @SpellViciousness; -- Viciousness
SET @WorgenRacial2                                             = @SpellAberration; -- Aberration
SET @WorgenRacial3                                             = @SpellFlayer; -- Flayer
SET @WorgenRacial4                                             = @SpellDarkflight; -- Darkflight
SET @TwoFormsMale                                              = @SpellTwoFormsMale;
SET @TwoFormsFemale                                            = @SpellTwoFormsFemale;
SET @HumanFormMale                                             = @SpellHumanFormMale;
SET @HumanFormFemale                                           = @SpellHumanFormFemale;
SET @RunningWildMale60                                         = @SpellRunningWildMale60; -- Running Wild: quadrupedal transform aura (male worgen) & +60% speed boost aura
SET @RunningWildFemale60                                       = @SpellRunningWildFemale60; -- Running Wild: quadrupedal transform aura (female worgen) & +60% speed boost aura
SET @RunningWildMale100                                        = @SpellRunningWildMale100; -- Running Wild: quadrupedal transform aura (male worgen) & +100% speed boost aura
SET @RunningWildFemale100                                      = @SpellRunningWildFemale100; -- Running Wild: quadrupedal transform aura (female worgen) & +100% speed boost aura
SET @GoblinRacial1                                             = @SpellRocketBarrage; -- Rocket Barrage
SET @GoblinRacial2                                             = @SpellTimeIsMoney; -- Time is Money
SET @GoblinRacial3                                             = @SpellBestDealsAnywhere; -- Best Deals Anywhere
SET @GoblinRacial4                                             = @SpellBetterLivingThroughChemistry; -- Better Living Through Chemistry
SET @GoblinRacial5                                             = @SpellPackHobgoblin; -- Pack Hobgoblin
SET @GoblinRacial6                                             = @SpellRocketJump; -- Rocket Jump
SET @HighElfRacial1                                            = @SpellQueldoreiMeditationDK; -- Quel’dorei Meditation (non-DK)
SET @HighElfRacial2                                            = @SpellSwiftnessOfTheRangers; -- Swiftness of the Rangers
SET @HighElfRacial3                                            = @SpellQueldoreiMeditation; -- Quel’dorei Meditation (DK)
SET @HighElfRacial4                                            = @SpellBowSpecialization; -- Bow Specialization
SET @HighElfRacial5                                            = @SpellEnchantingSpecialization; -- Enchanting Specialization
SET @MagharOrcRacial1                                          = @SpellAncestralCall; -- Ancestral Call
SET @MagharOrcRacial2                                          = @SpellSavageBlood; -- Savage Blood
SET @MagharOrcRacial3                                          = @SpellSympatheticVigor; -- Sympathetic Vigor
SET @MagharOrcRacial4                                          = @SpellOpenSkies; -- Open Skies (was Unwavering Will)
SET @DarkIronDwarfRacial1                                      = @SpellMoleMachine;
SET @DarkIronDwarfRacial2                                      = @SpellFireblood;
SET @DarkIronDwarfRacial3                                      = @SpellForgedInFlames;
SET @DarkIronDwarfRacial4                                      = @SpellMassProduction;
SET @DarkIronDwarfRacial5                                      = @SpellDungeonDelver;
SET @ZandalariTrollRacial1                                     = @SpellCityOfGold;
SET @ZandalariTrollRacial2                                     = @SpellEmbraceOfTheLoa1;
SET @ZandalariTrollRacial3                                     = @SpellEmbraceOfTheLoa2;
SET @ZandalariTrollRacial4                                     = @SpellPterrodaxSwoop;
SET @ZandalariTrollRacial5                                     = @SpellRegeneratin;
SET @VulperaRacial1                                            = @SpellAlpacaSaddlebags;
SET @VulperaRacial2                                            = @SpellBagOfTricks;
SET @VulperaRacial3                                            = @SpellFireResistance;
SET @VulperaRacial4                                            = @SpellMakeCamp;
SET @VulperaRacial5                                            = @SpellNoseForTrouble;
SET @VulperaRacial6                                            = @SpellReturnToCamp;
SET @VulperaRacial7                                            = @SpellRummageYourBag;
SET @PandarenRacial1                                           = @SpellBouncy;
SET @PandarenRacial2                                           = @SpellEpicurean;
SET @PandarenRacial3                                           = @SpellGourmand;
SET @PandarenRacial4                                           = @SpellInnerPeace;
SET @PandarenRacial5                                           = @SpellQuakingPalm;
SET @KulTiranRacial1                                           = @SpellHaymaker;
SET @KulTiranRacial2                                           = @SpellJackOfAllTrades;
SET @KulTiranRacial3                                           = @SpellBrushItOff;
SET @KulTiranRacial4                                           = @SpellChildOfTheSea;
SET @KulTiranRacial5                                           = @SpellRimeOfTheAncientMariner;
SET @VoidElfRacial1                                            = @SpellChillOfNight;
SET @VoidElfRacial2                                            = @SpellEntropicEmbrace;
SET @VoidElfRacial3                                            = @SpellEtherealConnection;
SET @VoidElfRacial4                                            = @SpellPreternaturalCalm;
SET @VoidElfRacial5                                            = @SpellSpatialRift;
SET @LightforgedDraeneiRacial1                                 = @SpellDemonbane;
SET @LightforgedDraeneiRacial2                                 = @SpellForgeOfLight1;
SET @LightforgedDraeneiRacial3                                 = @SpellForgeOfLight2;
SET @LightforgedDraeneiRacial4                                 = @SpellHolyProvidence;
SET @LightforgedDraeneiRacial5                                 = @SpellLightsJudgement;
SET @LightforgedDraeneiRacial6                                 = @SpellLightsReckoning;
-- SET @OgreRacial1
-- SET @BrokenRacial1
-- SET @NagaRacial1

-- Icons
SET @IconBestDealsAnywhere                                      =    4331; -- Goblin
SET @IconRocketLauncher                                         =  133032; -- Goblin
SET @IconDarkflight                                             =  366937; -- Worgen
SET @IconTimeIsMoney                                            =  369214; -- Goblin
SET @IconPackHobgoblin                                          =  370211; -- Goblin
SET @IconBetterLivingThroughChemistry                           =  370670; -- Goblin
SET @IconRocketJump                                             =  370769; -- Goblin
SET @IconGoblinAchievement                                      =  463874; -- Goblin
SET @IconWorgenAchievement                                      =  463876; -- Worgen
SET @IconRunningWild                                            =  514641; -- Worgen
SET @IconAncestralCall                                          = 2021574; -- Mag'har Orc
SET @IconOpenSkies                                              = 2021575; -- Mag'har Orc
SET @IconSavageBlood                                            = 2021576; -- Mag'har Orc
SET @IconSympatheticVigor                                       = 2021577; -- Mag'har Orc
SET @IconDungeonDelver                                          = 1786405; -- Dark Iron Dwarf
SET @IconFireblood                                              = 1786406; -- Dark Iron Dwarf
SET @IconForgedInFlames                                         = 1786407; -- Dark Iron Dwarf
SET @IconMassProduction                                         = 1786408; -- Dark Iron Dwarf
SET @IconMoleMachine                                            = 1786409; -- Dark Iron Dwarf
SET @IconCityOfGold                                             = 1850547; -- Zandalari Troll
SET @IconEmbraceTheLoa                                          = 1850548; -- Zandalari Troll
SET @IconPterrodaxSwoop                                         = 1850549; -- Zandalari Troll
SET @IconRegeneratin                                            = 1850550; -- Zandalari Troll
SET @IconVulperaMount                                           = 3045400; -- Caravan Hyena
SET @IconAlpacaSaddlebags                                       = 3193421; -- Vulpera
SET @IconBagOfTricks                                            = 3193416; -- Vulpera
SET @IconFireResistance                                         = 3193417; -- Vulpera
SET @IconMakeCamp                                               = 3193418; -- Vulpera
SET @IconNoseForTrouble                                         = 3193419; -- Vulpera
SET @IconReturnToCamp                                           = 3193420; -- Vulpera
SET @IconRummageYourBag                                         = 3193422; -- Vulpera
SET @IconDragonTurtleBlue                                       =  656343; -- Dragon Turtle
SET @IconDragonTurtlePurple                                     =  657918; -- Dragon Turtle
SET @IconDragonTurtleGreen                                      =  657917; -- Dragon Turtle
SET @IconDragonTurtleBlack                                      =  656342; -- Dragon Turtle
SET @IconBouncy                                                 =  572033; -- Pandaren
SET @IconEpicurean                                              =  571692; -- Pandaren
SET @IconGourmand                                               =  571693; -- Pandaren
SET @IconInnerPeace                                             =  572034; -- Pandaren
SET @IconQuakingPalm                                            =  572035; -- Pandaren
SET @IconBrushItOff                                             = 2447780; -- Kul Tiran
SET @IconChildOfTheSea                                          = 2447781; -- Kul Tiran
SET @IconHaymaker                                               = 2447782; -- Kul Tiran
SET @IconJackOfAllTrades                                        = 2447783; -- Kul Tiran
SET @IconRimeOfTheAncientMariner                                = 2447784; -- Kul Tiran
SET @IconHMMooseMount                                           = 1757668; -- Highmountain Tauren
SET @IconBullRush                                               = 1723987; -- Highmountain Tauren
SET @IconMountaineer                                            = 1723999; -- Highmountain Tauren
SET @IconPrideOfIronhorn                                        = 1724002; -- Highmountain Tauren
SET @IconRuggedTenacity                                         = 1724003; -- Highmountain Tauren
SET @IconWasteNotWantNot                                        = 1724005; -- Highmountain Tauren
SET @IconVoidElfStriderMount                                    =  156486; -- Void Elf
SET @IconChillOfNight                                           = 1723989; -- Void Elf
SET @IconEntropicEmbrace                                        = 1723992; -- Void Elf
SET @IconEtherealConnection                                     = 1723993; -- Void Elf
SET @IconPreternaturalCalm                                      = 1724001; -- Void Elf
SET @IconSpatialRift                                            = 1724004; -- Void Elf
SET @IconLightforgedElekk                                       = 1713157; -- Lightforged Draenei
SET @IconDemonbane                                              = 1723990; -- Lightforged Draenei
SET @IconForgeOfLight                                           = 1723995; -- Lightforged Draenei
SET @IconHolyProvidence                                         = 1723996; -- Lightforged Draenei
SET @IconLightsJudgement                                        = 1724000; -- Lightforged Draenei
SET @IconLightsReckoning                                        = 1723994; -- Lightforged Draenei

-- Other Relevant Spells
SET @ApprenticeSkinning                                         =    8613;
SET @JourneymanSkinning                                         =    8617;
SET @ExpertSkinning                                             =    8618;
SET @ArtisanSkinning                                            =   10768;
SET @Skinning1                                                  =   13697;
SET @MasterSkinning                                             =   32678;
SET @GrandMasterSkinning                                        =   50305;
SET @Skinning2                                                  =   52158;

-- Druid Form Models
SET @DruidBearWorgenModel                                      =    3516; -- Cataclysm ID
SET @DruidBearTrollModel                                       =    3517; -- Cataclysm ID
SET @DruidCatWorgenModel                                       =    3518; -- Cataclysm ID
SET @DruidCatTrollModel                                        =    3519; -- Cataclysm ID
SET @DruidTreeFormModel                                        =    3805; -- Cataclysm ID
SET @DruidFlightWorgenModel                                    =    3845; -- Cataclysm ID
SET @DruidFlightTrollModel                                     =    3846; -- Cataclysm ID
SET @DruidTravelAllianceModel                                  =    @NextModelID := @NextModelID +1; -- 4870;
SET @DruidTravelHordeModel                                     =    @NextModelID := @NextModelID +1; -- 4871;
SET @DruidFlightHighmountainTaurenModel                        =    @NextModelID := @NextModelID +1; -- 4872;
SET @DruidBearZandalariTrollModel                              =    @NextModelID := @NextModelID +1; -- 4873;
SET @DruidCatZandalariTrollModel                               =    @NextModelID := @NextModelID +1; -- 4874;
SET @DruidFlightZandalariTrollModel                            =    @NextModelID := @NextModelID +1; -- 4875;
SET @DruidMoonkinZandalariTrollModel                           =    @NextModelID := @NextModelID +1; -- 4876;
SET @DruidTravelZandalariTrollModel                            =    @NextModelID := @NextModelID +1; -- 4877;
SET @DruidAquaticZandalariTrollModel                           =    @NextModelID := @NextModelID +1; -- 4878;
SET @DruidBearHighmountainTaurenModel                          =    @NextModelID := @NextModelID +1; -- 4879;
SET @DruidCatHighmountainTaurenModel                           =    @NextModelID := @NextModelID +1; -- 4880;
SET @DruidMoonkinHighmountainTaurenModel                       =    @NextModelID := @NextModelID +1; -- 4881;
SET @DruidBearKulTiranModel                                    =    @NextModelID := @NextModelID +1; -- 4882;
SET @DruidCatKulTiranModel                                     =    @NextModelID := @NextModelID +1; -- 4883;
SET @DruidFlightKulTiranModel                                  =    @NextModelID := @NextModelID +1; -- 4884;
SET @DruidMoonkinKulTiranModel                                 =    @NextModelID := @NextModelID +1; -- 4885;
SET @DruidTravelKulTiranModel                                  =    @NextModelID := @NextModelID +1; -- 4886;
SET @DruidAquaticKulTiranModel                                 =    @NextModelID := @NextModelID +1; -- 4887;

-- Druid Form Display IDs
SET @DruidBearWorgenDisplay                                    =   @NextDisplayID := @NextDisplayID +1; -- 33650;
SET @DruidBearWorgenBlackDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 33651;
SET @DruidBearWorgenBrownDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 33652;
SET @DruidBearWorgenTanDisplay                                 =   @NextDisplayID := @NextDisplayID +1; -- 33653;
SET @DruidBearWorgenWhiteDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 33654;
SET @DruidBearTrollBlueDisplay                                 =   @NextDisplayID := @NextDisplayID +1; -- 33655;
SET @DruidBearTrollPurpleDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 33656;
SET @DruidBearTrollRedDisplay                                  =   @NextDisplayID := @NextDisplayID +1; -- 33657;
SET @DruidBearTrollWhiteDisplay                                =   @NextDisplayID := @NextDisplayID +1; -- 33658;
SET @DruidBearTrollYellowDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 33659;
SET @DruidCatSkinWorgenDisplay                                 =   @NextDisplayID := @NextDisplayID +1; -- 33660;
SET @DruidCatSkinWorgenBlackDisplay                            =   @NextDisplayID := @NextDisplayID +1; -- 33661;
SET @DruidCatSkinWorgenBrownDisplay                            =   @NextDisplayID := @NextDisplayID +1; -- 33662;
SET @DruidCatSkinWorgenWhiteDisplay                            =   @NextDisplayID := @NextDisplayID +1; -- 33663;
SET @DruidCatSkinWorgenYellowDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 33664;
SET @DruidCatTrollSkinBlackDisplay                             =   @NextDisplayID := @NextDisplayID +1; -- 33665;
SET @DruidCatTrollSkinBlueDisplay                              =   @NextDisplayID := @NextDisplayID +1; -- 33666;
SET @DruidCatTrollSkinGreenDisplay                             =   @NextDisplayID := @NextDisplayID +1; -- 33667;
SET @DruidCatTrollSkinRedDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 33668;
SET @DruidCatTrollSkinWhiteDisplay                             =   @NextDisplayID := @NextDisplayID +1; -- 33669;
SET @DruidCatSkinPurpleDisplay                                 =   @NextDisplayID := @NextDisplayID +1; -- 34521;
SET @DruidTreeFormGreenDisplay                                 =   @NextDisplayID := @NextDisplayID +1; -- 37163;
SET @DruidTreeFormRedDisplay                                   =   @NextDisplayID := @NextDisplayID +1; -- 37164;
SET @DruidTreeFormPurpleDisplay                                =   @NextDisplayID := @NextDisplayID +1; -- 37165;
SET @DruidTreeFormOrangeDisplay                                =   @NextDisplayID := @NextDisplayID +1; -- 37166;
SET @DruidOwlBearBlackSkinDisplay                              =   @NextDisplayID := @NextDisplayID +1; -- 37173;
SET @DruidOwlBearRedSkinDisplay                                =   @NextDisplayID := @NextDisplayID +1; -- 37174;
SET @StormCrowDruidSkinDisplay                                 =   @NextDisplayID := @NextDisplayID +1; -- 37727;
SET @EpicDruidFlightWorgenDisplay                              =   @NextDisplayID := @NextDisplayID +1; -- 37729;
SET @EpicDruidFlightTrollDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 37730;
SET @DruidFlightTrollDisplay                                   =   @NextDisplayID := @NextDisplayID +1; -- 94216;
SET @DruidTravelAllianceDisplay                                =   @NextDisplayID := @NextDisplayID +1; -- 40816;
SET @DruidTravelHordeDisplay                                   =   @NextDisplayID := @NextDisplayID +1; -- 45339;
SET @DruidFlightHighmountainTaurenDisplay                      =   @NextDisplayID := @NextDisplayID +1; -- 94160;
SET @DruidBearZandalariTrollBlueDisplay                        =   @NextDisplayID := @NextDisplayID +1; -- 94161;
SET @DruidBearZandalariTrollDarkDisplay                        =   @NextDisplayID := @NextDisplayID +1; -- 94162;
SET @DruidBearZandalariTrollGreenDisplay                       =   @NextDisplayID := @NextDisplayID +1; -- 94163;
SET @DruidBearZandalariTrollWhiteDisplay                       =   @NextDisplayID := @NextDisplayID +1; -- 94164;
SET @DruidCatZandalariTrollBlackDisplay                        =   @NextDisplayID := @NextDisplayID +1; -- 94165;
SET @DruidCatZandalariTrollBlueDisplay                         =   @NextDisplayID := @NextDisplayID +1; -- 94166;
SET @DruidCatZandalariTrollGreenDisplay                        =   @NextDisplayID := @NextDisplayID +1; -- 94167;
SET @DruidCatZandalariTrollWhiteDisplay                        =   @NextDisplayID := @NextDisplayID +1; -- 94168;
SET @DruidFlightZandalariTrollDisplay                          =   @NextDisplayID := @NextDisplayID +1; -- 94169;
SET @DruidMoonkinZandalariTrollDisplay                         =   @NextDisplayID := @NextDisplayID +1; -- 94170;
SET @DruidTravelZandalariTrollDisplay                          =   @NextDisplayID := @NextDisplayID +1; -- 94171;
SET @DruidTreeZandalariTrollDisplay                            =   @NextDisplayID := @NextDisplayID +1; -- 94172;
SET @DruidAquaticZandalariTrollTealDisplay                     =   @NextDisplayID := @NextDisplayID +1; -- 94173;
SET @DruidAquaticZandalariTrollDarkDisplay                     =   @NextDisplayID := @NextDisplayID +1; -- 94174;
SET @DruidAquaticZandalariTrollGreenDisplay                    =   @NextDisplayID := @NextDisplayID +1; -- 94175;
SET @DruidAquaticZandalariTrollLightDisplay                    =   @NextDisplayID := @NextDisplayID +1; -- 94176;
SET @DruidBearHighmountainTaurenBlackDisplay                   =   @NextDisplayID := @NextDisplayID +1; -- 94177;
SET @DruidBearHighmountainTaurenBrownDisplay                   =   @NextDisplayID := @NextDisplayID +1; -- 94178;
SET @DruidBearHighmountainTaurenSilverDisplay                  =   @NextDisplayID := @NextDisplayID +1; -- 94179;
SET @DruidBearHighmountainTaurenWhiteDisplay                   =   @NextDisplayID := @NextDisplayID +1; -- 94180;
SET @DruidBearHighmountainTaurenYellowDisplay                  =   @NextDisplayID := @NextDisplayID +1; -- 94181;
SET @DruidCatHighmountainTaurenBlackDisplay                    =   @NextDisplayID := @NextDisplayID +1; -- 94182;
SET @DruidCatHighmountainTaurenBrownDisplay                    =   @NextDisplayID := @NextDisplayID +1; -- 94183;
SET @DruidCatHighmountainTaurenRedDisplay                      =   @NextDisplayID := @NextDisplayID +1; -- 94184;
SET @DruidCatHighmountainTaurenWhiteDisplay                    =   @NextDisplayID := @NextDisplayID +1; -- 94185;
SET @DruidMoonkinHighmountainTaurenDisplay                     =   @NextDisplayID := @NextDisplayID +1; -- 94186;
SET @DruidBearKulTiranBrownDisplay                             =   @NextDisplayID := @NextDisplayID +1; -- 94187;
SET @DruidBearKulTiranDarkDisplay                              =   @NextDisplayID := @NextDisplayID +1; -- 94188;
SET @DruidBearKulTiranGreenDisplay                             =   @NextDisplayID := @NextDisplayID +1; -- 94189;
SET @DruidBearKulTiranLightDisplay                             =   @NextDisplayID := @NextDisplayID +1; -- 94190;
SET @DruidCatKulTiranBrownDisplay                              =   @NextDisplayID := @NextDisplayID +1; -- 94191;
SET @DruidCatKulTiranDarkDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 94192;
SET @DruidCatKulTiranGreenDisplay                              =   @NextDisplayID := @NextDisplayID +1; -- 94193;
SET @DruidCatKulTiranLightDisplay                              =   @NextDisplayID := @NextDisplayID +1; -- 94194;
SET @DruidFlightKulTiranBrownDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94195;
SET @DruidFlightKulTiranDarkDisplay                            =   @NextDisplayID := @NextDisplayID +1; -- 94196;
SET @DruidFlightKulTiranGreenDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94197;
SET @DruidFlightKulTiranLightDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94198;
SET @DruidMoonkinKulTiranDisplay                               =   @NextDisplayID := @NextDisplayID +1; -- 94199;
SET @DruidMoonkinKulTiranBlackDisplay                          =   @NextDisplayID := @NextDisplayID +1; -- 94200;
SET @DruidMoonkinKulTiranPaleDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94201;
SET @DruidMoonkinKulTiranRedDisplay                            =   @NextDisplayID := @NextDisplayID +1; -- 94202;
SET @DruidTravelKulTiranBlueDisplay                            =   @NextDisplayID := @NextDisplayID +1; -- 94203;
SET @DruidTravelKulTiranBrownDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94204;
SET @DruidTravelKulTiranGreenDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94205;
SET @DruidTravelKulTiranWhiteDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94206;
SET @DruidAquaticKulTiranBrownDisplay                          =   @NextDisplayID := @NextDisplayID +1; -- 94207;
SET @DruidAquaticKulTiranDarkDisplay                           =   @NextDisplayID := @NextDisplayID +1; -- 94208;
SET @DruidAquaticKulTiranGreenDisplay                          =   @NextDisplayID := @NextDisplayID +1; -- 94209;
SET @DruidAquaticKulTiranLightDisplay                          =   @NextDisplayID := @NextDisplayID +1; -- 94210;
SET @DruidTreeKulTiranDisplay                                  =   @NextDisplayID := @NextDisplayID +1; -- 94214;

-- Weapon Skills
SET @SwordSkill                                                =       43;
SET @AxeSkill                                                  =       44;
SET @BowSkill                                                  =       45;
SET @GunSkill                                                  =       46;
SET @MaceSkill                                                 =       54;
SET @DualWieldSkill                                            =      118;
SET @StaveSkill                                                =      136;
SET @2HMaceSkill                                               =      160;
SET @2HAxeSkill                                                =      172;
SET @DaggerSkill                                               =      173;
SET @CrossbowSkill                                             =      226;
SET @PolearmSkill                                              =      229;
SET @FistWeaponSkill                                           =      473;

-- Gear Skills
SET @PlateMailSkill                                            =      293;
SET @MailSkill                                                 =      413;
SET @LeatherSkill                                              =      414;
SET @ClothSkill                                                =      415;
SET @ShieldSkill                                               =      433;

-- Language Skills
SET @CommonSkill                                               =       98;
SET @OrcishSkill                                               =      109;
SET @DraconicSkill                                             =      138;
SET @DemonTongueSkill                                          =      139;
SET @TitanSkill                                                =      140;
SET @OldTongueSkill                                            =      141;

-- Profession Skills
SET @SurvivalSkill                                             =      142;
SET @AlchemySkill                                              =      171;
SET @BlacksmithingSkill                                        =      164;
SET @LeatherworkingSkill                                       =      165;
SET @HerbalismSkill                                            =      182;
SET @CookingSkill                                              =      185;
SET @MiningSkill                                               =      186;
SET @TailoringSkill                                            =      197;
SET @EngineeringSkill                                          =      202;
SET @EnchantingSkill                                           =      333;
SET @FishingSkill                                              =      356;
SET @SkinningSkill                                             =      393;
SET @JewelcraftingSkill                                        =      755;

-- Racial SkillLineAbility
SET @BloodFuryWarlockSkillLineAbility                          =    15034; -- Orc Warlock
SET @BloodFuryShamanSkillLineAbility                           =    15035; -- Orc Shaman
SET @ElusivenessSkillLineAbility                               =    20665; -- Night Elf
SET @ArcaneTorrentManaSkillLineAbility                         =    14013; -- Blood Elf Paladin, Hunter, Priest, Mage, Warlock
SET @ArcaneTorrentDKSkillLineAbility                           =    17510; -- Blood Elf DK
SET @HeroicPresenceMailClassesSkillLineAbility                 =    14022; -- Draenei Warrior, Paladin, Hunter, DK
SET @HeroicPresenceCasterClassesSkillLineAbility               =    14023; -- Draenei Priest, Shaman, Mage
SET @ShadowResistanceDKSkillLineAbility                        =    20171; -- Draenei DK
SET @ArcaneTorrentFeralSkillLineAbility                        =    31450;
SET @ArcaneTorrentDruidManaSkillLineAbility                    =    31451;
SET @ArcaneTorrentRageSkillLineAbility                         =    31452;
SET @GiftoftheNaaruDruidSkillLineAbility                       =    31453;
SET @GiftoftheNaaruRogueSkillLineAbility                       =    31454;
SET @GiftoftheNaaruWarlockSkillLineAbility                     =    31455;
SET @ShadowResistanceDruidSkillLineAbility                     =    31456;
SET @ShadowResistanceRogueSkillLineAbility                     =    31457;
SET @ShadowResistanceWarlockSkillLineAbility                   =    31458;
SET @WorgenSkillLineAbility1                                   =    21981;
SET @WorgenSkillLineAbility2                                   =    21982;
SET @WorgenSkillLineAbility3                                   =    21983;
SET @WorgenSkillLineAbility4                                   =    21984;
SET @GoblinSkillLineAbility1                                   =    21985;
SET @GoblinSkillLineAbility2                                   =    21986;
SET @GoblinSkillLineAbility3                                   =    21987;
SET @GoblinSkillLineAbility4                                   =    21988;
SET @GoblinSkillLineAbility5                                   =    21989;
SET @GoblinSkillLineAbility6                                   =    31448;
SET @MagharOrcSkillLineAbility1                                =    31459;
SET @MagharOrcSkillLineAbility2                                =    31460;
SET @MagharOrcSkillLineAbility3                                =    31461;
SET @MagharOrcSkillLineAbility4                                =    31462;
SET @HighElfSkillLineAbility1                                  =    31463;
SET @HighElfSkillLineAbility2                                  =    31464;
SET @HighElfSkillLineAbility3                                  =    31465;
SET @HighElfSkillLineAbility4                                  =    31466;
SET @HighElfSkillLineAbility5                                  =    31467;
SET @DarkIronDwarfSkillLineAbility1                            =    31468;
SET @DarkIronDwarfSkillLineAbility2                            =    31469;
SET @DarkIronDwarfSkillLineAbility3                            =    31470;
SET @DarkIronDwarfSkillLineAbility4                            =    31471;
SET @DarkIronDwarfSkillLineAbility5                            =    31472;
SET @HighmountainTaurenSkillLineAbility1                       =    31473;
SET @HighmountainTaurenSkillLineAbility2                       =    31474;
SET @HighmountainTaurenSkillLineAbility3                       =    31475;
SET @HighmountainTaurenSkillLineAbility4                       =    31476;
SET @HighmountainTaurenSkillLineAbility5                       =    31477;
SET @VoidElfSkillLineAbility1                                  =    31478;
SET @VoidElfSkillLineAbility2                                  =    31479;
SET @VoidElfSkillLineAbility3                                  =    31480;
SET @VoidElfSkillLineAbility4                                  =    31481;
SET @VoidElfSkillLineAbility5                                  =    31482;
SET @LightforgedDraeneiSkillLineAbility1                       =    31483;
SET @LightforgedDraeneiSkillLineAbility2                       =    31484;
SET @LightforgedDraeneiSkillLineAbility3                       =    31485;
SET @LightforgedDraeneiSkillLineAbility4                       =    31486;
SET @LightforgedDraeneiSkillLineAbility5                       =    31487;
SET @LightforgedDraeneiSkillLineAbility6                       =    31488;
SET @ZandalariTrollSkillLineAbility1                           =    31489;
SET @ZandalariTrollSkillLineAbility2                           =    31490;
SET @ZandalariTrollSkillLineAbility3                           =    31491;
SET @ZandalariTrollSkillLineAbility4                           =    31492;
SET @ZandalariTrollSkillLineAbility5                           =    31493;

-- Language SkillLineAbility
SET @OrcishSkillLineAbilityHorde                               =      592;
SET @CommonSkillLineAbilityAlliance                            =      590;
SET @ThalassianSkillLineAbility                                =      727;

-- Teleport SkillLineAbility
SET @TeleportDarnassusSkillLineAbility                         =     3269;
SET @TeleportIronforgeSkillLineAbility                         =     3270;
SET @TeleportStormwindSkillLineAbility                         =     3272;
SET @TeleportExodarSkillLineAbility                            =    14815;
SET @TeleportShattrathSkillLineAbilityAlliance                 =    15040;
SET @TeleportTheramoreSkillLineAbility                         =    16999;
SET @TeleportOrgrimmarSkillLineAbility                         =     3271;
SET @TeleportThunderBluffSkillLineAbility                      =     3273;
SET @TeleportUndercitySkillLineAbility                         =     3274;
SET @TeleportSilvermoonSkillLineAbility                        =    14816;
SET @TeleportShattrathSkillLineAbilityHorde                    =    15606;
SET @TeleportStonardSkillLineAbility                           =    17000;

-- Portal SkillLineAbility
SET @PortalDarnassusSkillLineAbility                           =     5989;
SET @PortalIronforgeSkillLineAbility                           =     5990;
SET @PortalStormwindSkillLineAbility                           =     5992;
SET @PortalExodarSkillLineAbility                              =    14817;
SET @PortalShattrathSkillLineAbilityAlliance                   =    15041;
SET @PortalTheramoreSkillLineAbility                           =    17004;
SET @PortalOrgrimmarSkillLineAbility                           =     5991;
SET @PortalThunderBluffSkillLineAbility                        =     5993;
SET @PortalUndercitySkillLineAbility                           =     5994;
SET @PortalSilvermoonSkillLineAbility                          =    14818;
SET @PortalShattrathSkillLineAbilityHorde                      =    15607;
SET @PortalStonardSkillLineAbility                             =    17003;

-- Paladin SkillLineAbility
SET @HolyVengeanceSkillLineAbility                             =    14787; -- Alliance paladin
SET @SealofVengeanceSkillLineAbility                           =    14779; -- Alliance paladin
SET @JudgementofVengeanceSkillLineAbility                      =    14788; -- Alliance paladin
SET @JudgementoftheMartyrSkillLineAbility                      =    18299; -- Alliance paladin
SET @WarhorseSkillLineAbility1                                 =     7594; -- Alliance paladin (60%)
SET @WarhorseSkillLineAbility2                                 =    20091; -- Alliance paladin (60%)
SET @ChargerSkillLineAbility1                                  =    12518; -- Alliance paladin (100%)
SET @ChargerSkillLineAbility2                                  =    20089; -- Alliance paladin (100%)
SET @JudgementofBloodSkillLineAbility                          =    14784; -- Blood Elf paladin
SET @JudgementofCorruptionSkillLineAbility                     =    18308; -- Blood Elf paladin
SET @SealofCorruptionSkillLineAbility                          =    18311; -- Blood Elf paladin
SET @BloodCorruptionSkillLineAbility                           =    18314; -- Blood Elf paladin
SET @SummonChargerSkillLineAbility1                            =    15252; -- Blood Elf paladin (100%)
SET @SummonChargerSkillLineAbility2                            =    20090; -- Blood Elf paladin (100%)
SET @SummonWarhorseSkillLineAbility1                           =    15253; -- Blood Elf paladin (60%)
SET @SummonWarhorseSkillLineAbility2                           =    20092; -- Blood Elf paladin (60%)

-- Shaman SkillLineAbility
SET @BloodlustSkillLineAbility                                 =    13151; -- Horde shaman
SET @HeroismSkillLineAbility                                   =    14795; -- Draenei shaman
SET @FlameShockPassiveSkillLineAbility                         =    21724;

-- Miscellaneous SkillLineAbility
SET @MekgineersChopperSkillLineAbility1                        =    20283; -- Alliance
SET @MekgineersChopperSkillLineAbility2                        =    20289; -- Alliance
SET @MechanoHogSkillLineAbility1                               =    20110; -- Horde
SET @MechanoHogSkillLineAbility2                               =    20290; -- Horde
SET @ActivatePrimarySpec                                       =    20867;
SET @ActivateSecondarySpec                                     =    20868;

-- Racial SkillRaceClass
SET @WorgenRacialSkillRaceClass                                =      971;
SET @GoblinRacialSkillRaceClass                                =      972;
SET @HighElfRacialSkillRaceClass                               =     1140;
SET @MagharOrcRacialSkillRaceClass                             =     1141;
SET @OgreRacialSkillRaceClass                                  =     1142;
SET @DarkIronDwarfRacialSkillRaceClass                         =     1143;
SET @GilneanRacialSkillRaceClass                               =     1144; -- For completion's sake
SET @HighmountainTaurenRacialSkillRaceClass                    =     1145;
SET @NagaRacialSkillRaceClass                                  =     1146;
SET @TaunkaRacialSkillRaceClass                                =     1147;
SET @VoidElfRacialSkillRaceClass                               =     1148;
SET @LightforgedDraeneiRacialSkillRaceClass                    =     1149;
SET @ZandalariTrollRacialSkillRaceClass                        =     1150;
SET @VulperaRacialSkillRaceClass                               =     1151;
SET @BrokenRacialSkillRaceClass                                =     1152;
SET @PandarenRacialSkillRaceClass                              =     1153;

-- Weapon SkillRaceClass
SET @AxesHunterSkillRaceClass1                                 =      117; -- Hunter: Orc, Dwarf, Tauren, Troll
SET @2HAxePaladinSkillRaceClass                                =      122; -- Paladin (up to bit 18)
SET @DaggersRogueWarlockSkillRaceClass                         =      129; -- Rogue, warlock (up to bit 15)
SET @GunsHunterStartSkillRaceClass                             =      133; -- Hunter
SET @GunsNonHunterSkillRaceClass                               =      134; -- Warrior, Rogue
SET @MacesPriestShamanSkillRaceClass                           =      135; -- Priest, Shaman
SET @SwordsWarriorSkillRaceClass                               =      140; -- Warrior, except Dwarf, Tauren, Troll (they are in 140 for some reason)
SET @SwordsHunterSkillRaceClass                                =      328; -- Hunter, except Draenei (they are alone in 880 for some reason)
SET @FistWeaponsSkillRaceClass                                 =      330; -- Warrior, Hunter, Rogue, Shaman, Druid
SET @AxesOtherSkillRaceClass                                   =      335; -- Paladin, Rogue, Shaman
SET @DaggersCastersSkillRaceClass                              =      323; -- Priest, Shaman, Mage (up to bit 15)
SET @2HAxeWarriorSkillRaceClass                                =      622; -- Warrior, except Orc, Dwarf (they are in 621 for some reason)
SET @2HMaceSkillRaceClass1                                     =      624; -- Warrior, Tauren
SET @2HMaceSkillRaceClass2                                     =      625; -- Warrior, except Tauren for some reason
SET @AxesHunterSkillRaceClass2                                 =      628; -- Hunter: Night Elf, Blood Elf, Draenei
SET @AxesWarriorSkillRaceClass1                                =      629; -- Warrior: Human, Orc, Dwarf, Tauren, Troll
SET @AxesWarriorSkillRaceClass2                                =      630; -- Warrior: Night Elf, Undead, Gnome, Draenei
SET @DaggersHunterSkillRaceClass1                              =      631; -- Hunter: Night Elf, Blood Elf
SET @DaggersHunterSkillRaceClass2                              =      632; -- Hunter: Orc, Dwarf, Tauren, Troll, Draenei
SET @DaggersWarriorSkillRaceClass1                             =      633; -- Warrior: Night Elf, Undead, Gnome, Troll
SET @DaggersWarriorSkillRaceClass2                             =      634; -- Warrior: Human, Orc, Dwarf, Tauren, Draenei
SET @GunsHunterLearnSkillRaceClass                             =      635; -- Hunter
SET @MacesWarriorSkillRaceClass1                               =      636; -- Warrior: Human, Dwarf, Night Elf, Tauren, Gnome, Draenei
SET @MacesWarriorSkillRaceClass2                               =      637; -- Warrior: Orc, Undead, Troll, Blood Elf
SET @DaggersDruidTaurenSkillRaceClass                          =      641; -- Druid: Tauren
SET @DaggersDruidNightElfSkillRaceClass                        =      642; -- Druid: Night Elf
SET @MacesDruidNightElfSkillRaceClass                          =      643; -- Druid: Night Elf
SET @MacesDruidTaurenSkillRaceClass                            =      644; -- Druid: Tauren
SET @2HAxeShamanSkillRaceClass                                 =      701; -- Shaman (up to bit 18)
SET @SwordsRogueSkillRaceClass                                 =      872; -- Rogue
SET @SwordsMageWarlockSkillRaceClass                           =      881; -- Mage, Warlock
SET @SwordsPaladinSkillRaceClass                               =      885; -- Paladin (Alliance: Human, Dwarf, Draenei)
SET @SwordsPaladinHordeSkillRaceClass                          =      886; -- Paladin (Horde: Blood Elf)
SET @MacesPaladinSkillRaceClass                                =      888; -- Paladin, except Blood Elf (up to bit 18)
SET @MacesPaladinBloodElfSkillRaceClass                        =      889; -- Paladin: Blood Elf
SET @2HAxeDKSkillRaceClass                                     =      907; -- DK (up to bit 19)
SET @SwordsDKSkillRaceClass                                    =      910; -- DK (up to bit 18)
SET @AxesDKSkillRaceClass                                      =      912; -- DK (up to bit 18)
SET @MacesDKSkillRaceClass                                     =      914; -- DK (up to bit 18)
SET @2HAxeHunterSkillRaceClass                                 =      970; -- Hunter (up to bit 18)
SET @StavesCastersSkillRaceClass                               =      138; -- Priest, Shaman, Mage, Warlock, Druid (up to bit 15)
SET @StavesWarriorHunterSkillRaceClass                         =      139; -- Warrior, Hunter (up to bit 15)
SET @PolearmsSkillRaceClass                                    =      229; -- Warrior, Paladin, Hunter, Druid (up to bit 15)
SET @PolearmsDKSkillRaceClass                                  =      915; -- DK (up to bit 18)
SET @DualWieldRogueSkillRaceClass                              =      131; -- Rogue (up to bit 15)
SET @DualWieldWarriorHunterSkillRaceClass                      =      132; -- Warrior, Hunter (up to bit 15)
SET @DualWieldShamanSkillRaceClass                             =      883; -- Shaman (up to bit 15)
SET @DualWieldDKSkillRaceClass                                 =      913; -- DK (up to bit 18)

-- Gear SkillRaceClass
SET @PlateMailSkillRaceClass                                   =       21; -- Warrior, paladin
SET @PlateMailDKSkillRaceClass                                 =      906; -- DK
SET @Mail40SkillRaceClass                                      =      145;
SET @MailSkillRaceClass                                        =      146;
SET @LeatherSkillRaceClass                                     =      147;
SET @ClothSkillRaceClass                                       =      148;
SET @ShieldSkillRaceClass                                      =      246;

-- Language SkillRaceClass
SET @CommonSkillRaceClassAlliance                              =       40;
SET @CommonSkillRaceClassHorde                                 =       41;
SET @OrcishSkillRaceClassHorde                                 =       48;
SET @OrcishSkillRaceClassAlliance                              =       49;
SET @DemonTongueSkillRaceClass                                 =       84;
SET @DraconicSkillRaceClass                                    =       85;
SET @OldTongueSkillRaceClass                                   =       88;
SET @TitanSkillRaceClass                                       =       93;
SET @GutterspeakSkillRaceClass                                 =      742; -- Everyone except undead

-- Profession SkillRaceClass
SET @FishingSkillRaceClass                                     =       27;
SET @HerbalismSkillRaceClass                                   =       28;
SET @MiningSkillRaceClass                                      =       29;
SET @SkinningSkillRaceClass                                    =       30;
SET @AlchemySkillRaceClass                                     =      241;
SET @BlacksmithingSkillRaceClass                               =      243;
SET @EngineeringSkillRaceClass                                 =      244;
SET @EnchantingSkillRaceClass                                  =      281;
SET @CookingSkillRaceClass                                     =      282;
SET @TailoringSkillRaceClass                                   =      284;
SET @SurvivalSkillRaceClass                                    =      865;
SET @JewelcraftingSkillRaceClass                               =      866;
SET @LeatherworkingSkillRaceClass                              =      899;

-- Riding SkillRaceClass
SET @HorseRidingHumanSkillRaceClass                            =       87; -- Human
SET @RamRidingDwarfSkillRaceClass                              =       89; -- Dwarf
SET @TigerRidingNightElfSkillRaceClass                         =       92; -- Night Elf
SET @WolfRidingOrcSkillRaceClass                               =       94; -- Orc
SET @HorseRidingGeneralSkillRaceClass                          =      441; -- Orc, Dwarf, Night Elf, Undead, Gnome, Troll (no Tauren, Blood Elf or Draenei)
SET @RamRidingGeneralSkillRaceClass                            =      442; -- Human, Orc, Night Elf, Undead, Gnome, Troll (no Tauren, Blood Elf or Draenei)
SET @WolfRidingGeneralSkillRaceClass                           =      443; -- Human, Dwarf, Night Elf, Undead, Tauren, Gnome, Troll, Goblin (no Blood Elf or Draenei)
SET @RaptorRidingGeneralSkillRaceClass                         =      446; -- Human, Orc, Dwarf, Night Elf, Undead, Gnome
SET @MechanostriderPilotingGnomeSkillRaceClass                 =      461; -- Gnome
SET @UndeadHorsemanshipGeneralSkillRaceClass                   =      463; -- Human, Orc, Dwarf, Night Elf, Gnome, Troll
SET @TigerRidingGeneralSkillRaceClass                          =      481; -- Human, Orc, Dwarf, Undead, Gnome, Troll
SET @MechanostriderPilotingDwarfSkillRaceClass                 =      501; -- Dwarf

-- Mount Models
SET @HorseModel                                                =       65;
SET @GoblinTrikeModel                                          =     3623;
SET @GoblinTurboTrikeModel                                     =     3624;
SET @CaravanHyena1Model                                        =     @NextModelID := @NextModelID +1; -- 3628; -- Vacant slot
SET @CaravanHyena2Model                                        =     @NextModelID := @NextModelID +1; -- 3629; -- Vacant slot
SET @DragonTurtleModel                                         =     @NextModelID := @NextModelID +1; -- 3630; -- Vacant slot
SET @HighmountainThunderhoofModel                              =     @NextModelID := @NextModelID +1; -- 3631; -- Vacant slot
SET @LightforgedFelcrusherModel                                =     @NextModelID := @NextModelID +1; -- 3632; -- Vacant slot
SET @NightborneManasaberModel                                  =     @NextModelID := @NextModelID +1;
SET @StarcursedVoidstriderModel                                =     @NextModelID := @NextModelID +1;
SET @MechagonMechanostriderModel                               =     @NextModelID := @NextModelID +1;
SET @MagharDirewolfModel                                       =     @NextModelID := @NextModelID +1;
SET @KulTiranChargerModel                                      =     @NextModelID := @NextModelID +1;
SET @DarkIronCoreHoundModel                                    =     @NextModelID := @NextModelID +1;
SET @ZandalariDirehornModel                                    =     @NextModelID := @NextModelID +1;
SET @CrimsonVorquinModel                                       =     @NextModelID := @NextModelID +1;
SET @SapphireVorquinModel                                      =     @NextModelID := @NextModelID +1;
SET @ObsidianVorquinModel                                      =     @NextModelID := @NextModelID +1;
SET @BronzeVorquinModel                                        =     @NextModelID := @NextModelID +1;
SET @GuardianVorquinModel                                      =     @NextModelID := @NextModelID +1;
SET @ArmoredVorquinLeystriderModel                             =     @NextModelID := @NextModelID +1;
SET @MajesticArmoredVorquinModel                               =     @NextModelID := @NextModelID +1;
SET @SlatestoneRamolithModel                                   =     @NextModelID := @NextModelID +1;
SET @RootstalkerGrimlynxModel                                  =     @NextModelID := @NextModelID +1;
SET @DuskGrimlynxModel                                         =     @NextModelID := @NextModelID +1;
SET @IvoryGrimlynxModel                                        =     @NextModelID := @NextModelID +1;
SET @FierceGrimlynxModel                                       =     @NextModelID := @NextModelID +1;
SET @UmberGalestriderModel                                     =     @NextModelID := @NextModelID +1;
SET @StormyGalestriderModel                                    =     @NextModelID := @NextModelID +1;
SET @EmpyreanGalestriderModel                                  =     @NextModelID := @NextModelID +1;
SET @SwiftUmberGalestriderModel                                =     @NextModelID := @NextModelID +1;
SET @SwiftStormyGalestriderModel                               =     @NextModelID := @NextModelID +1;
SET @SwiftEmpyreanGalestriderModel                             =     @NextModelID := @NextModelID +1;

-- Mount Display IDs
SET @GoblinTrikeDisplay                                        =    35249; -- Cataclysm ID?
SET @GoblinTurboTrikeDisplay                                   =    35250; -- Cataclysm ID?
SET @MountainHorseDisplay                                      =    39095; -- black, Cataclysm ID?
SET @SwiftMountainHorseDisplay                                 =    39096; -- brown, Cataclysm ID?
SET @CaravanHyena1Display                                      =    @NextModelID := @NextModelID +1; -- 94211; -- vacant slot
SET @CaravanHyena2Display                                      =    @NextModelID := @NextModelID +1; -- 94212; -- vacant slot
SET @DragonTurtleBlueDisplay                                   =    @NextModelID := @NextModelID +1; -- 94228; -- vacant slot
SET @DragonTurtlePurpleDisplay                                 =    @NextModelID := @NextModelID +1; -- 94229; -- vacant slot
SET @DragonTurtleGreenDisplay                                  =    @NextModelID := @NextModelID +1; -- 94230; -- vacant slot
SET @DragonTurtleBlackDisplay                                  =    @NextModelID := @NextModelID +1; -- 94231; -- vacant slot
SET @HighmountainThunderhoofDisplay                            =    @NextModelID := @NextModelID +1; -- 94232; -- vacant slot
SET @LightforgedFelcrusherPurpleDisplay                        =    @NextModelID := @NextModelID +1; -- 94233; -- vacant slot
SET @LightforgedFelcrusherBlueDisplay                          =    @NextModelID := @NextModelID +1; -- 94234; -- vacant slot
SET @LightforgedFelcrusherDarkDisplay                          =    @NextModelID := @NextModelID +1; -- 94235; -- vacant slot
SET @LightforgedFelcrusherHolyDisplay                          =    @NextModelID := @NextModelID +1; -- 94236; -- vacant slot
SET @NightborneManasaberDisplay                                =    @NextModelID := @NextModelID +1;
SET @StarcursedVoidstriderDisplay                              =    @NextModelID := @NextModelID +1;
SET @MechagonMechanostriderDisplay                             =    @NextModelID := @NextModelID +1;
SET @MagharDirewolfDisplay                                     =    @NextModelID := @NextModelID +1;
SET @KulTiranChargerDisplay                                    =    @NextModelID := @NextModelID +1;
SET @DarkIronCoreHoundDisplay                                  =    @NextModelID := @NextModelID +1;
SET @ZandalariDirehornDisplay                                  =    @NextModelID := @NextModelID +1;
SET @CrimsonVorquinDisplay                                     =    @NextModelID := @NextModelID +1;
SET @SapphireVorquinDisplay                                    =    @NextModelID := @NextModelID +1;
SET @ObsidianVorquinDisplay                                    =    @NextModelID := @NextModelID +1;
SET @BronzeVorquinDisplay                                      =    @NextModelID := @NextModelID +1;
SET @GuardianVorquinDisplay                                    =    @NextModelID := @NextModelID +1;
SET @ArmoredVorquinLeystriderDisplay                           =    @NextModelID := @NextModelID +1;
SET @MajesticArmoredVorquinDisplay                             =    @NextModelID := @NextModelID +1;
SET @SlatestoneRamolithDisplay                                 =    @NextModelID := @NextModelID +1;
SET @RootstalkerGrimlynxDisplay                                =    @NextModelID := @NextModelID +1;
SET @DuskGrimlynxDisplay                                       =    @NextModelID := @NextModelID +1;
SET @IvoryGrimlynxDisplay                                      =    @NextModelID := @NextModelID +1;
SET @FierceGrimlynxDisplay                                     =    @NextModelID := @NextModelID +1;
SET @UmberGalestriderDisplay                                   =    @NextModelID := @NextModelID +1;
SET @StormyGalestriderDisplay                                  =    @NextModelID := @NextModelID +1;
SET @EmpyreanGalestriderDisplay                                =    @NextModelID := @NextModelID +1;
SET @SwiftUmberGalestriderDisplay                              =    @NextModelID := @NextModelID +1;
SET @SwiftStormyGalestriderDisplay                             =    @NextModelID := @NextModelID +1;
SET @SwiftEmpyreanGalestriderDisplay                           =    @NextModelID := @NextModelID +1;

-- Creature IDs
SET @GobberCreatureID                                          =    36613; -- Cataclysm ID
SET @GoblinTrikeCreatureID                                     =    46754; -- Cataclysm ID
SET @GoblinTurboTrikeCreatureID                                =    46755; -- Cataclysm ID
SET @MountainHorseCreatureID                                   =    55272; -- Cataclysm ID
SET @SwiftMountainHorseCreatureID                              =    55273; -- Cataclysm ID
SET @CaravanHyena1CreatureID                                   =   @NextCreatureID := @NextCreatureID +1; -- 182781; -- vacant slot
SET @CaravanHyena2CreatureID                                   =   @NextCreatureID := @NextCreatureID +1; -- 182782; -- vacant slot
SET @DragonTurtleBlueCreatureID                                =   @NextCreatureID := @NextCreatureID +1; -- 182783; -- vacant slot
SET @DragonTurtlePurpleCreatureID                              =   @NextCreatureID := @NextCreatureID +1; -- 182784; -- vacant slot
SET @DragonTurtleGreenCreatureID                               =   @NextCreatureID := @NextCreatureID +1; -- 182785; -- vacant slot
SET @DragonTurtleBlackCreatureID                               =   @NextCreatureID := @NextCreatureID +1; -- 182786; -- vacant slot
SET @HighmountainThunderhoofCreatureID                         =   @NextCreatureID := @NextCreatureID +1; -- 182787; -- vacant slot
SET @LightforgedFelcrusherPurpleCreatureID                     =   @NextCreatureID := @NextCreatureID +1; -- 182788; -- vacant slot
SET @LightforgedFelcrusherBlueCreatureID                       =   @NextCreatureID := @NextCreatureID +1; -- 182789; -- vacant slot
SET @LightforgedFelcrusherDarkCreatureID                       =   @NextCreatureID := @NextCreatureID +1; -- 182790; -- vacant slot
SET @LightforgedFelcrusherHolyCreatureID                       =   @NextCreatureID := @NextCreatureID +1; -- 182791; -- vacant slot
SET @NightborneManasaberCreatureID                             =   @NextCreatureID := @NextCreatureID +1;
SET @StarcursedVoidstriderCreatureID                           =   @NextCreatureID := @NextCreatureID +1;
SET @MechagonMechanostriderCreatureID                          =   @NextCreatureID := @NextCreatureID +1;
SET @MagharDirewolfCreatureID                                  =   @NextCreatureID := @NextCreatureID +1;
SET @KulTiranChargerCreatureID                                 =   @NextCreatureID := @NextCreatureID +1;
SET @DarkIronCoreHoundCreatureID                               =   @NextCreatureID := @NextCreatureID +1;
SET @ZandalariDirehornCreatureID                               =   @NextCreatureID := @NextCreatureID +1;
SET @CrimsonVorquinCreatureID                                  =   @NextCreatureID := @NextCreatureID +1;
SET @SapphireVorquinCreatureID                                 =   @NextCreatureID := @NextCreatureID +1;
SET @ObsidianVorquinCreatureID                                 =   @NextCreatureID := @NextCreatureID +1;
SET @BronzeVorquinCreatureID                                   =   @NextCreatureID := @NextCreatureID +1;
SET @GuardianVorquinCreatureID                                 =   @NextCreatureID := @NextCreatureID +1;
SET @ArmoredVorquinLeystriderCreatureID                        =   @NextCreatureID := @NextCreatureID +1;
SET @MajesticArmoredVorquinCreatureID                          =   @NextCreatureID := @NextCreatureID +1;
SET @SlatestoneRamolithCreatureID                              =   @NextCreatureID := @NextCreatureID +1;
SET @RootstalkerGrimlynxCreatureID                             =   @NextCreatureID := @NextCreatureID +1;
SET @DuskGrimlynxCreatureID                                    =   @NextCreatureID := @NextCreatureID +1;
SET @IvoryGrimlynxCreatureID                                   =   @NextCreatureID := @NextCreatureID +1;
SET @FierceGrimlynxCreatureID                                  =   @NextCreatureID := @NextCreatureID +1;
SET @UmberGalestriderCreatureID                                =   @NextCreatureID := @NextCreatureID +1;
SET @StormyGalestriderCreatureID                               =   @NextCreatureID := @NextCreatureID +1;
SET @EmpyreanGalestriderCreatureID                             =   @NextCreatureID := @NextCreatureID +1;
SET @SwiftUmberGalestriderCreatureID                           =   @NextCreatureID := @NextCreatureID +1;
SET @SwiftStormyGalestriderCreatureID                          =   @NextCreatureID := @NextCreatureID +1;
SET @SwiftEmpyreanGalestriderCreatureID                        =   @NextCreatureID := @NextCreatureID +1;

-- Mount Items
SET @GoblinTrikeItem                                           =    62461; -- Cataclysm ID
SET @GoblinTurboTrikeItem                                      =    62462; -- Cataclysm ID
SET @MountainHorseItem                                         =    73838; -- Cataclysm ID
SET @SwiftMountainHorseItem                                    =    73839; -- Cataclysm ID
SET @CaravanHyena1Item                                         =   174066; -- BfA ID
SET @CaravanHyena2Item                                         =   174065; -- Uses BfA ID of Titan Core
SET @DragonTurtleBlueItem                                      =    91009; -- MoP ID
SET @DragonTurtlePurpleItem                                    =    91006; -- MoP ID
SET @DragonTurtleGreenItem                                     =    91004; -- MoP ID
SET @DragonTurtleBlackItem                                     =    91008; -- MoP ID
SET @NightborneManasaberItem                                   =   156487; -- Legion ID
SET @HighmountainThunderhoofItem                               =   155662; -- Legion ID
SET @LightforgedFelcrusherHolyItem                             =   155656; -- Legion ID
SET @LightforgedFelcrusherPurpleItem                           =   174067; -- vacant slot
SET @LightforgedFelcrusherBlueItem                             =   174068; -- vacant slot
SET @LightforgedFelcrusherDarkItem                             =   174069; -- vacant slot
SET @StarcursedVoidstriderItem                                 =   156486; -- Legion ID
SET @MagharDirewolfItem                                        =   161330; -- BfA ID
SET @DarkIronCoreHoundItem                                     =   161331; -- BfA ID
SET @KulTiranChargerItem                                       =   164762; -- BfA ID
SET @MechagonMechanostriderItem                                =   174067; -- BfA ID
SET @ZandalariDirehornItem                                     =   157870; -- BfA ID
SET @CrimsonVorquinItem                                        =   201702; -- Dragonflight ID
SET @SapphireVorquinItem                                       =   201704; -- Dragonflight ID
SET @ObsidianVorquinItem                                       =   201719; -- Dragonflight ID
SET @BronzeVorquinItem                                         =   201720; -- Dragonflight ID
SET @GuardianVorquinItem                                       =   198808; -- Dragonflight ID
SET @ArmoredVorquinLeystriderItem                              =   198809; -- Dragonflight ID
SET @MajesticArmoredVorquinItem                                =   198811; -- Dragonflight ID
SET @SlatestoneRamolithItem                                    =   223572; -- Dragonflight ID
SET @IvoryGrimlynxItem                                         =   246736; -- Midnight ID
SET @FierceGrimlynxItem                                        =   246734; -- Midnight ID
SET @RootstalkerGrimlynxItem                                   =   223572; -- Midnight ID
SET @DuskGrimlynxItem                                          =   246731; -- Midnight ID
SET @UmberGalestriderItem                                      =   274930; -- Forever ID
SET @StormyGalestriderItem                                     =   269683; -- Forever ID
SET @EmpyreanGalestriderItem                                   =   269681; -- Forever ID
SET @SwiftUmberGalestriderItem                                 =   274933; -- Forever ID
SET @SwiftStormyGalestriderItem                                =   269678; -- Forever ID
SET @SwiftEmpyreanGalestriderItem                              =   269671; -- Forever ID

SET @NextItemDisplayID                                         =   132261;
-- Mount Item Display ID
SET @GoblinTrikeItemDisplay                                    =   134237; -- Cataclysm ID?
SET @GoblinTurboTrikeItemDisplay                               =   134238; -- Cataclysm ID?
SET @MountainHorseItemDisplay                                  =   132261; -- Cataclysm ID?
SET @SwiftMountainHorseItemDisplay                             =   @MountainHorseItemDisplay;
SET @CaravanHyena1ItemDisplay                                  =   @NextItemDisplayID := @NextItemDisplayID +1; -- 132262; -- vacant slot
SET @CaravanHyena2ItemDisplay                                  =   @CaravanHyena1ItemDisplay;
SET @DragonTurtleBlueItemDisplay                               =   @NextItemDisplayID := @NextItemDisplayID +1; -- 132263; -- vacant slot
SET @DragonTurtlePurpleItemDisplay                             =   @NextItemDisplayID := @NextItemDisplayID +1; -- 132264; -- vacant slot
SET @DragonTurtleGreenItemDisplay                              =   @NextItemDisplayID := @NextItemDisplayID +1; -- 132265; -- vacant slot
SET @DragonTurtleBlackItemDisplay                              =   @NextItemDisplayID := @NextItemDisplayID +1; -- 132266; -- vacant slot
SET @HighmountainThunderhoofItemDisplay                        =   @NextItemDisplayID := @NextItemDisplayID +1; -- 132267; -- vacant slot
SET @LightforgedFelcrusherHolyItemDisplay                      =   @NextItemDisplayID := @NextItemDisplayID +1; -- 132268; -- vacant slot
SET @LightforgedFelcrusherPurpleItemDisplay                    =   @LightforgedFelcrusherHolyItemDisplay;
SET @LightforgedFelcrusherBlueItemDisplay                      =   @LightforgedFelcrusherHolyItemDisplay;
SET @LightforgedFelcrusherDarkItemDisplay                      =   @LightforgedFelcrusherHolyItemDisplay;
SET @NightborneManasaberItemDisplay                            =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @StarcursedVoidstriderItemDisplay                          =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @MechagonMechanostriderItemDisplay                         =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @MagharDirewolfItemDisplay                                 =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @KulTiranChargerItemDisplay                                =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @DarkIronCoreHoundItemDisplay                              =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @ZandalariDirehornItemDisplay                              =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @CrimsonVorquinItemDisplay                                 =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @SapphireVorquinItemDisplay                                =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @ObsidianVorquinItemDisplay                                =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @BronzeVorquinItemDisplay                                  =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @GuardianVorquinItemDisplay                                =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @ArmoredVorquinLeystriderItemDisplay                       =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @MajesticArmoredVorquinItemDisplay                         =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @SlatestoneRamolithItemDisplay                             =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @RootstalkerGrimlynxItemDisplay                            =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @DuskGrimlynxItemDisplay                                   =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @IvoryGrimlynxItemDisplay                                  =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @FierceGrimlynxItemDisplay                                 =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @UmberGalestriderItemDisplay                               =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @StormyGalestriderItemDisplay                              =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @EmpyreanGalestriderItemDisplay                            =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @SwiftUmberGalestriderItemDisplay                          =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @SwiftStormyGalestriderItemDisplay                         =   @NextItemDisplayID := @NextItemDisplayID +1;
SET @SwiftEmpyreanGalestriderItemDisplay                       =   @NextItemDisplayID := @NextItemDisplayID +1;

-- Mount Spells
SET @GoblinTrike                                               =    87090; -- Cataclysm ID
SET @GoblinTurboTrike                                          =    87091; -- Cataclysm ID
SET @MountainHorse                                             =   103195; -- Cataclysm ID
SET @SwiftMountainHorse                                        =   103196; -- Cataclysm ID
SET @CaravanHyena1                                             =   306423; -- BfA ID
SET @CaravanHyena2                                             =   306424; -- Uses BfA ID of Unlocking
SET @DragonTurtleBlue                                          =   127287; -- MoP ID
SET @DragonTurtlePurple                                        =   127289; -- MoP ID
SET @DragonTurtleGreen                                         =   120395; -- MoP ID
SET @DragonTurtleBlack                                         =   127286; -- MoP ID
SET @HighmountainThunderhoof                                   =   258060; -- Legion ID
SET @LightforgedFelcrusherHoly                                 =   258022; -- Legion ID
SET @LightforgedFelcrusherPurple                               =   306425; -- vacant slot
SET @LightforgedFelcrusherBlue                                 =   306426; -- vacant slot
SET @LightforgedFelcrusherDark                                 =   306427; -- vacant slot
SET @DarkIronCoreHound                                         =   271646; -- BfA ID
SET @NightborneManasaber                                       =   258845; -- Legion ID
SET @StarcursedVoidstrider                                     =   259202; -- Legion ID
SET @ZandalariDirehorn                                         =   263707; -- BfA ID
SET @MagharDirewolf                                            =   267274; -- BfA ID
SET @KulTiranCharger                                           =   282682; -- BfA ID
SET @MechagonMechanostrider                                    =   305592; -- BfA ID
SET @CrimsonVorquin                                            =   394216; -- Dragonflight ID
SET @SapphireVorquin                                           =   394218; -- Dragonflight ID
SET @ObsidianVorquin                                           =   394220; -- Dragonflight ID
SET @BronzeVorquin                                             =   394219; -- Dragonflight ID
SET @GuardianVorquin                                           =   384963; -- Dragonflight ID
SET @ArmoredVorquinLeystrider                                  =   385134; -- Dragonflight ID
SET @MajesticArmoredVorquin                                    =   385115; -- Dragonflight ID
SET @SlatestoneRamolith                                        =   449415; -- TWW ID
SET @RootstalkerGrimlynx                                       =  1243597; -- Midnight ID
SET @DuskGrimlynx                                              =  1243582; -- Midnight ID
SET @IvoryGrimlynx                                             =  1243598; -- Midnight ID
SET @FierceGrimlynx                                            =  1243593; -- Midnight ID
SET @UmberGalestrider                                          =  1295678; -- Forever ID
SET @StormyGalestrider                                         =  1286026; -- Forever ID
SET @EmpyreanGalestrider                                       =  1286024; -- Forever ID
SET @SwiftUmberGalestrider                                     =  1295683; -- Forever ID
SET @SwiftStormyGalestrider                                    =  1286022; -- Forever ID
SET @SwiftEmpyreanGalestrider                                  =  1286011; -- Forever ID

-- Faction Masks
SET @VanillaAllianceMask                                       = @HumanMask           | @DwarfMask  | @NightElfMask  | @GnomeMask;
SET @VanillaHordeMask                                          = @OrcMask             | @UndeadMask | @TaurenMask    | @TrollMask;
SET @BaseAllianceMask                                          = @VanillaAllianceMask | @DraeneiMask;
SET @BaseHordeMask                                             = @VanillaHordeMask    | @BloodElfMask;
SET @AllianceMask                                              = @BaseAllianceMask; -- | @WorgenMask | @HighElfMask   | @DarkIronDwarfMask | @AlliancePandarenMask | @KulTiranMask;
SET @HordeMask                                                 = @BaseHordeMask;    -- | @GoblinMask | @MagharOrcMask | @OgreMask          | @ZandalariTrollMask | @VulperaMask;
SET @UndercityMask                                             = @UndeadMask          | @BloodElfMask; -- Mostly for easy reputation split
SET @BarrensBros                                               = @HordeMask           & ~@UndercityMask; -- Mostly for easy reputation split
SET @PlayableRaceMask                                          = @AllianceMask        | @HordeMask;
SET @GunHunters                                                = @DwarfMask           | @TaurenMask | @GnomeMask;
SET @CrossbowHunters                                           = @DraeneiMask         | @HumanMask  | @UndeadMask;
SET @BowHunters                                                = @PlayableRaceMask    & ~(@GunHunters | @CrossbowHunters);
SET @DaggersRogueOnly                                          = @TaurenMask          | @DraeneiMask;

-- Race and PLAYER factions (stock races)
SET @HumanFaction                                              =     72; -- Stormwind
SET @HumanPlayer                                               =      1;
SET @OrcFaction                                                =     76; -- Orgrimmar
SET @OrcPlayer                                                 =      2;
SET @DwarfFaction                                              =     47; -- Ironforge
SET @DwarfPlayer                                               =      3;
SET @NightElfFaction                                           =     69; -- Darnassus
SET @NightElfPlayer                                            =      4;
SET @UndeadFaction                                             =     68; -- Undercity
SET @UndeadPlayer                                              =      5;
SET @TaurenFaction                                             =     81; -- Thunder Bluff
SET @TaurenPlayer                                              =      6;
SET @GnomeFaction                                              =     54; -- Gnomeregan Exiles
SET @GnomePlayer                                               =      8;
SET @TrollFaction                                              =    530; -- Darkspear Trolls
SET @TrollPlayer                                               =      9;
SET @BloodElfFaction                                           =    911; -- Silvermoon City
SET @BloodElfPlayer                                            =    914;
SET @DraeneiFaction                                            =    930; -- Exodar
SET @DraeneiPlayer                                             =    927;

-- Race and PLAYER factions (retroported races)
SET @GoblinFaction                                             =     1133; -- Bilgewater Cartel (Cataclysm ID)
SET @GoblinPlayer                                              =     1152; -- Cataclysm ID
SET @WorgenFaction                                             =     1134; -- Gilneas (Cataclysm ID)
SET @WorgenPlayer                                              =     1153; -- Cataclysm ID
SET @AlliancePandarenFaction                                   =     1353; -- Tushui Pandaren (MoP ID)
SET @AlliancePandarenPlayer                                    =     1178; -- Vacant slot
SET @HordePandarenFaction                                      =     1352; -- Huojin Pandaren (MoP ID)
SET @HordePandarenPlayer                                       =     1180; -- Vacant slot
SET @VoidElfFaction                                            =     2170; -- Argussion Reach (Legion ID)
SET @VoidElfPlayer                                             =     2229; -- Legion ID
SET @HighmountainTaurenFaction                                 =     1828; -- Highmountain Tribe (Legion ID)
SET @HighmountainTaurenPlayer                                  =     2230; -- Legion ID
SET @NightborneFaction                                         =     1859; -- The Nightfallen (Legion ID)
SET @NightbornePlayer                                          =     2231; -- Legion ID
SET @LightforgedDraeneiFaction                                 =     2165; -- Army of the Light (Legion ID)
SET @LightforgedDraeneiPlayer                                  =     2232; -- Legion ID
SET @ZandalariTrollFaction                                     =     2103; -- Zandalari Empire (BfA ID)
SET @ZandalariTrollPlayer                                      =     1174; -- Vacant slot
SET @KulTiranFaction                                           =     2160; -- Proudmoore Admiralty (BfA ID)
SET @KulTiranPlayer                                            =     1184;
SET @DarkIronDwarfFaction                                      =     1171; -- Shadowforge City
SET @DarkIronDwarfPlayer                                       =     1172;
SET @VulperaFaction                                            =     2158; -- Voldunai (BfA ID)
SET @VulperaPlayer                                             =     1176;

-- Race and PLAYER factions (custom races)
SET @HighElfFaction                                            =     1167; -- High Elf Loyalists
SET @HighElfPlayer                                             =     1161;
SET @MagharOrcFaction                                          =     1168; -- Mag'har of the Horde
SET @MagharOrcPlayer                                           =     1166;
SET @BrokenFaction                                             =     1181;
SET @BrokenPlayer                                              =     1182; -- Broken of the Alliance
SET @OgreFaction                                               =     1170; -- Stonemaul Clan
SET @OgrePlayer                                                =     1169;
SET @GilneanFaction                                            =     1185;
SET @GilneanPlayer                                             =     1186;
SET @NagaFaction                                               =     1187;
SET @NagaPlayer                                                =     1188;
SET @TaunkaFaction                                             =     2231; -- Taunka of the Horde
SET @TaunkaPlayer                                              =     2232; -- vacant slot

-- Faction templates
SET @GoblinFactionTemplate                                     =     2238; -- References @GoblinPlayer
SET @WorgenFactionTemplate                                     =     2239; -- References @WorgenPlayer
SET @HighElfFactionTemplate                                    =     2237; -- References @HighElfPlayer
SET @MagharOrcFactionTemplate                                  =     2240; -- References @MagharOrcPlayer
SET @OgreFactionTemplate                                       =     2241; -- References @OgrePlayer
SET @DarkIronDwarfFactionTemplate                              =     2242; -- References @DarkIronDwarfPlayer
SET @ZandalariTrollFactionTemplate                             =     2243; -- References @ZandalariTrollPlayer
SET @VulperaFactionTemplate                                    =     2244; -- References @VulperaPlayer
SET @AlliancePandarenFactionTemplate                           =     2245; -- References @AlliancePandarenPlayer
SET @HordePandarenFactionTemplate                              =     2246; -- References @HordePandarenPlayer
SET @BrokenFactionTemplate                                     =     2247; -- References @BrokenPlayer
SET @KulTiranFactionTemplate                                   =     2248; -- References @KulTiranPlayer
SET @GilneanFactionTemplate                                    =     2249; -- References @GilneanPlayer
SET @HighmountainTaurenFactionTemplate                         =     2250; -- References @HighmountainTaurenPlayer
SET @NagaFactionTemplate                                       =     2251; -- References @NagaPlayer
SET @TaunkaFactionTemplate                                     =     2252; -- References @TaunkaPlayer
SET @VoidElfFactionTemplate                                    =     2253; -- References @VoidElfPlayer
SET @LightforgedDraeneiFactionTemplate                         =     2254; -- References @LightforgedDraeneiPlayer

-- Reputation Indices
SET @GoblinFactionRepIndex                                     =    105;
SET @WorgenFactionRepIndex                                     =    106;
SET @HighElfFactionRepIndex                                    =    107;
SET @MagharOrcFactionRepIndex                                  =    108;
SET @OgreFactionRepIndex                                       =    109;
SET @DarkIronDwarfFactionRepIndex                              =    110;
SET @ZandalariTrollFactionRepIndex                             =    111;
SET @VulperaFactionRepIndex                                    =    112;
SET @AlliancePandarenFactionRepIndex                           =    113;
SET @HordePandarenFactionRepIndex                              =    114;
SET @BrokenFactionRepIndex                                     =    115;
SET @KulTiranFactionRepIndex                                   =    116;
SET @GilneanFactionRepIndex                                    =    117;
SET @HighmountainTaurenFactionRepIndex                         =    118;
SET @NagaFactionRepIndex                                       =    119;
SET @TaunkaFactionRepIndex                                     =    120;
SET @VoidElfFactionRepIndex                                    =    121;
SET @LightforgedDraeneiFactionRepIndex                         =    122;

-- Achievements
SET @KnowThyEnemyAlliance                                      =     246;
SET @KnowThyEnemyHorde                                         =    1005;
SET @ShakeYourBunnyMaker                                       =    2422;
SET @CheckYourHead                                             =     291;
SET @GoblinAchievement                                         =    1429;
SET @WorgenAchievement                                         =    1430;
SET @HighElfAchievement                                        =    1431;
SET @MagharOrcAchievement                                      =    1432;
SET @OgreAchievement                                           =    1433;
SET @DarkIronDwarfAchievement                                  =    1434;
SET @ZandalariTrollAchievement                                 =    1435;
SET @VulperaAchievement                                        =    1436;
SET @AlliancePandarenAchievement                               =    1437;
SET @HordePandarenAchievement                                  =    1438;
SET @BrokenAchievement                                         =    1439;
SET @KulTiranAchievement                                       =    1440;
SET @GilneanAchievement                                        =    1441; -- For completion's sake
SET @HighmountainTaurenAchievement                             =    1442;
SET @NagaAchievement                                           =    1443;
SET @TaunkaAchievement                                         =    1444;
SET @VoidElfAchievement                                        =    1445;
SET @LightforgedDraeneiAchievement                             =    1446;

SET @Level80AchievementDescriptionenUS                         = 'Level to 80';
SET @Level80AchievementDescriptionkoKR                         = '80 레벨';
SET @Level80AchievementDescriptionfrFR                         = 'Atteindre le niveau 80';
SET @Level80AchievementDescriptiondeDE                         = 'Erreicht Stufe 80';
SET @Level80AchievementDescriptionzhCN                         = '升到80级';
SET @Level80AchievementDescriptionzhTW                         = '升至80級';
SET @Level80AchievementDescriptionesES                         = 'Alcanza el nivel 80';
SET @Level80AchievementDescriptionesMX                         = 'Alcanza el nivel 80';
SET @Level80AchievementDescriptionruRU                         = 'Достигнуть 80-го уровня';
SET @Level80AchievementDescriptionptPT                         = '';
SET @Level80AchievementDescriptionptBR                         = '';
SET @Level80AchievementDescriptionitIT                         = '';

-- Achievement Criteria
SET @GoblinCriteria1                                           =    13471; -- Achievement 1005: Know Thy Enemy
SET @GoblinCriteria2                                           =    13473; -- Achievement 2422: Shake Your Bunny-Maker
SET @GoblinCriteria3                                           =    13475; -- Achievement 291: Check Your Head
SET @GoblinCriteria4                                           =    13477; -- @GoblinAchievement: Realm First! Level 80 Goblin
SET @WorgenCriteria1                                           =    13472; -- Achievement 246: Know Thy Enemy
SET @WorgenCriteria2                                           =    13474; -- Achievement 2422: Shake Your Bunny-Maker
SET @WorgenCriteria3                                           =    13476; -- Achievement 291: Check Your Head
SET @WorgenCriteria4                                           =    13478; -- @WorgenAchievement: Realm First! Level 80 Worgen
SET @HighElfCriteria1                                          =    13484; -- Achievement 246: Know Thy Enemy
SET @HighElfCriteria2                                          =    13485; -- Achievement 2422: Shake Your Bunny-Maker
SET @HighElfCriteria3                                          =    19215; -- Achievement 291: Check Your Head
SET @HighElfCriteria4                                          =    19216; -- @HighElfAchievement: Realm First! Level 80 High Elf
SET @MagharOrcCriteria1                                        =    13498; -- Achievement 1005: Know Thy Enemy
SET @MagharOrcCriteria2                                        =    13499; -- Achievement 2422: Shake Your Bunny-Maker
SET @MagharOrcCriteria3                                        =    13500; -- Achievement 291: Check Your Head
SET @MagharOrcCriteria4                                        =    19217; -- @MagharOrcAchievement: Realm First! Level 80 Mag'har Orc
SET @OgreCriteria1                                             =    19218; -- Achievement 1005: Know Thy Enemy
SET @OgreCriteria2                                             =    19219; -- Achievement 2422: Shake Your Bunny-Maker
SET @OgreCriteria3                                             =    19220; -- Achievement 291: Check Your Head
SET @OgreCriteria4                                             =    19221; -- @OgreAchievement: Realm First! Level 80 Ogre
SET @DarkIronDwarfCriteria1                                    =    19222; -- Achievement 246: Know Thy Enemy
SET @DarkIronDwarfCriteria2                                    =    19223; -- Achievement 2422: Shake Your Bunny-Maker
SET @DarkIronDwarfCriteria3                                    =    19224; -- Achievement 291: Check Your Head
SET @DarkIronDwarfCriteria4                                    =    19225; -- @DarkIronDwarfAchievement: Realm First! Level 80 Dark Iron Dwarf
SET @ZandalariTrollCriteria1                                   =    19226; -- Achievement 1005: Know Thy Enemy
SET @ZandalariTrollCriteria2                                   =    19227; -- Achievement 2422: Shake Your Bunny-Maker
SET @ZandalariTrollCriteria3                                   =    19228; -- Achievement 291: Check Your Head
SET @ZandalariTrollCriteria4                                   =    19229; -- @ZandalariTrollAchievement: Realm First! Level 80 Zandalari Troll
SET @VulperaCriteria1                                          =    19230; -- Achievement 1005: Know Thy Enemy
SET @VulperaCriteria2                                          =    19231; -- Achievement 2422: Shake Your Bunny-Maker
SET @VulperaCriteria3                                          =    19232; -- Achievement 291: Check Your Head
SET @VulperaCriteria4                                          =    19233; -- @VulperaAchievement: Realm First! Level 80 Vulpera
SET @AlliancePandarenCriteria1                                 =    19234; -- Achievement 246: Know Thy Enemy
SET @AlliancePandarenCriteria2                                 =    19235; -- Achievement 2422: Shake Your Bunny-Maker
SET @AlliancePandarenCriteria3                                 =    19236; -- Achievement 291: Check Your Head
SET @AlliancePandarenCriteria4                                 =    19237; -- @AlliancePandarenAchievement: Realm First! Level 80 Pandaren (Alliance)
SET @HordePandarenCriteria1                                    =    19238; -- Achievement 1005: Know Thy Enemy
SET @HordePandarenCriteria2                                    =    19239; -- Achievement 2422: Shake Your Bunny-Maker
SET @HordePandarenCriteria3                                    =    19240; -- Achievement 291: Check Your Head
SET @HordePandarenCriteria4                                    =    19241; -- @HordePandarenAchievement: Realm First! Level 80 Pandaren (Horde)
SET @HighmountainTaurenCriteria1                               =    19242; -- Achievement 1005: Know Thy Enemy
SET @HighmountainTaurenCriteria2                               =    19243; -- Achievement 2422: Shake Your Bunny-Maker
SET @HighmountainTaurenCriteria3                               =    19244; -- Achievement 291: Check Your Head
SET @HighmountainTaurenCriteria4                               =    19245; -- @HighmountainTaurenAchievement: Realm First! Level 80 Highmountain Tauren
SET @NagaCriteria1                                             =    19246; -- Achievement 1005: Know Thy Enemy
SET @NagaCriteria2                                             =    19247; -- Achievement 2422: Shake Your Bunny-Maker
SET @NagaCriteria3                                             =    19248; -- Achievement 291: Check Your Head
SET @NagaCriteria4                                             =    19249; -- @NagaAchievement: Realm First! Level 80 Naga
SET @BrokenCriteria1                                           =    19250; -- Achievement 246: Know Thy Enemy
SET @BrokenCriteria2                                           =    19251; -- Achievement 2422: Shake Your Bunny-Maker
SET @BrokenCriteria3                                           =    19252; -- Achievement 291: Check Your Head
SET @BrokenCriteria4                                           =    19253; -- @BrokenAchievement: Realm First! Level 80 Broken
SET @KulTiranCriteria1                                         =    19254; -- Achievement 246: Know Thy Enemy
SET @KulTiranCriteria2                                         =    19255; -- Achievement 2422: Shake Your Bunny-Maker
SET @KulTiranCriteria3                                         =    19256; -- Achievement 291: Check Your Head
SET @KulTiranCriteria4                                         =    19257; -- @KulTiranAchievement: Realm First! Level 80 Kul Tiran
SET @GilneanCriteria1                                          =    19258; -- Achievement 246: Know Thy Enemy
SET @GilneanCriteria2                                          =    19259; -- Achievement 2422: Shake Your Bunny-Maker
SET @GilneanCriteria3                                          =    19260; -- Achievement 291: Check Your Head
SET @GilneanCriteria4                                          =    19261; -- @GilneanAchievement: Realm First! Level 80 Gilnean
SET @TaunkaCriteria1                                           =    19262; -- Achievement 1005: Know Thy Enemy
SET @TaunkaCriteria2                                           =    19263; -- Achievement 2422: Shake Your Bunny-Maker
SET @TaunkaCriteria3                                           =    19264; -- Achievement 291: Check Your Head
SET @TaunkaCriteria4                                           =    19265; -- @NagaAchievement: Realm First! Level 80 Naga
SET @VoidElfCriteria1                                          =    19266; -- Achievement 246: Know Thy Enemy
SET @VoidElfCriteria2                                          =    19267; -- Achievement 2422: Shake Your Bunny-Maker
SET @VoidElfCriteria3                                          =    19268; -- Achievement 291: Check Your Head
SET @VoidElfCriteria4                                          =    19269; -- @VoidElfAchievement: Realm First! Level 80 Void Elf
SET @LightforgedDraeneiCriteria1                               =    19270; -- Achievement 246: Know Thy Enemy
SET @LightforgedDraeneiCriteria2                               =    19271; -- Achievement 2422: Shake Your Bunny-Maker
SET @LightforgedDraeneiCriteria3                               =    19272; -- Achievement 291: Check Your Head
SET @LightforgedDraeneiCriteria4                               =    19273; -- @LightforgedDraeneiAchievement: Realm First! Level 80 Lightforged Draenei

-- Classes
SET @Warrior                                                   =      1;
SET @Paladin                                                   =      2;
SET @Hunter                                                    =      3;
SET @Rogue                                                     =      4;
SET @Priest                                                    =      5;
SET @DeathKnight                                               =      6;
SET @Shaman                                                    =      7;
SET @Mage                                                      =      8;
SET @Warlock                                                   =      9;
-- SET @Monk                                                      =     10;
SET @Druid                                                     =     11;

-- ClassMasks
SET @WarriorMask                                               =   1 << (@Warrior     - 1);  -- class ID 1  → 1
SET @PaladinMask                                               =   1 << (@Paladin     - 1);  -- class ID 2  → 2
SET @HunterMask                                                =   1 << (@Hunter      - 1);  -- class ID 3  → 4
SET @RogueMask                                                 =   1 << (@Rogue       - 1);  -- class ID 4  → 8
SET @PriestMask                                                =   1 << (@Priest      - 1);  -- class ID 5  → 16
SET @DeathKnightMask                                           =   1 << (@DeathKnight - 1);  -- class ID 6  → 32
SET @ShamanMask                                                =   1 << (@Shaman      - 1);  -- class ID 7  → 64
SET @MageMask                                                  =   1 << (@Mage        - 1);  -- class ID 8  → 128
SET @WarlockMask                                               =   1 << (@Warlock     - 1);  -- class ID 9  → 256
-- SET @MonkMask                                                  =   1 << (@Monk        - 1); -- class ID 10 → 512
SET @DruidMask                                                 =   1 << (@Druid       - 1); -- class ID 11 → 1024

SET @AllClassMask                                              = @WarriorMask  | @PaladinMask | @HunterMask | @RogueMask | @PriestMask | @DeathKnightMask | @ShamanMask | @MageMask | @WarlockMask | @DruidMask;
SET @ManaClassMask                                             = @PaladinMask  | @HunterMask | @PriestMask | @ShamanMask | @MageMask | @WarlockMask | @DruidMask;
SET @NonDKMask                                                 = @AllClassMask & ~@DeathKnightMask;

-- Druid Forms
SET @CatForm                                                   =           1;
SET @TreeForm                                                  =           2;
SET @TravelForm                                                =           3;
SET @AquaticForm                                               =           4;
SET @BearForm                                                  =           5;
SET @DireBearForm                                              =           8;
SET @SwiftFlightForm                                           =          27;
SET @FlightForm                                                =          29;
SET @MoonkinForm                                               =          31;

SET @AllianceTravelForm                                        =       40816;
SET @HordeTravelForm                                           =       45339;

-- Orc totems
SET @OrcFireTotem                                              =       30758;
SET @OrcEarthTotem                                             =       30757;
SET @OrcWaterTotem                                             =       30759;
SET @OrcAirTotem                                               =       30756;

-- Dwarf totems
SET @DwarfFireTotem                                            =       30754;
SET @DwarfEarthTotem                                           =       30753;
SET @DwarfWaterTotem                                           =       30755;
SET @DwarfAirTotem                                             =       30736;

-- Tauren totems
SET @TaurenFireTotem                                           =        4589;
SET @TaurenEarthTotem                                          =        4588;
SET @TaurenWaterTotem                                          =        4587;
SET @TaurenAirTotem                                            =        4590;

-- Troll totems
SET @TrollFireTotem                                            =       30762;
SET @TrollEarthTotem                                           =       30761;
SET @TrollWaterTotem                                           =       30763;
SET @TrollAirTotem                                             =       30760;

-- Draenei totems
SET @DraeneiFireTotem                                          =       19074;
SET @DraeneiEarthTotem                                         =       19073;
SET @DraeneiWaterTotem                                         =       19075;
SET @DraeneiAirTotem                                           =       19071;

-- Default totems Alliance
SET @AllianceFireTotem                                         =       @DwarfFireTotem;
SET @AllianceEarthTotem                                        =       @DwarfEarthTotem;
SET @AllianceWaterTotem                                        =       @DwarfWaterTotem;
SET @AllianceAirTotem                                          =       @DwarfAirTotem;

-- Default totems Horde
SET @HordeFireTotem                                            =       @OrcFireTotem;
SET @HordeEarthTotem                                           =       @OrcEarthTotem;
SET @HordeWaterTotem                                           =       @OrcWaterTotem;
SET @HordeAirTotem                                             =       @OrcAirTotem;

-- Locations
SET @EasternKingdoms                                           =           0;
SET @DunMorogh                                                 =           1;
SET @ElwynnForest                                              =          12;
SET @TirisfalGlades                                            =          85;
SET @Gilneas                                                   =        4714; -- Open Azeroth
SET @GilneasCity                                               =        4755; -- Open Azeroth

SET @Kalimdor                                                  =           1;
SET @Durotar                                                   =          14;
SET @Teldrassil                                                =         141;
SET @Mulgore                                                   =         215;
SET @Kezan                                                     =        4737; -- Open Azeroth
SET @LostIsles                                                 =        4720; -- Open Azeroth

SET @Outland                                                   =         530;
SET @AzuremystIsle                                             =        3526; -- Outland map
SET @EversongWoods                                             =        3431; -- Outland map

SET @Northrend                                                 =         609;
SET @ScarletEnclave                                            =        4298;

-- Start coordinates

SET @HumanStartX                                                =   -8949.95;
SET @HumanStartY                                                =   -132.493;
SET @HumanStartZ                                                =    83.5312;
SET @HumanStartO                                                =          0;

SET @OrcStartX                                                  =   -618.518;
SET @OrcStartY                                                  =   -4251.67;
SET @OrcStartZ                                                  =     38.718;
SET @OrcStartO                                                  =          0;

SET @DwarfStartX                                                =   -6240.32;
SET @DwarfStartY                                                =    331.033;
SET @DwarfStartZ                                                =    382.758;
SET @DwarfStartO                                                =    6.17716;

SET @NightElfStartX                                             =    10311.3;
SET @NightElfStartY                                             =    832.463;
SET @NightElfStartZ                                             =    1326.41;
SET @NightElfStartO                                             =    5.69632;

SET @UndeadStartX                                               =    1676.71;
SET @UndeadStartY                                               =    1678.31;
SET @UndeadStartZ                                               =     121.67;
SET @UndeadStartO                                               =    2.70526;

SET @TaurenStartX                                               =   -2917.58;
SET @TaurenStartY                                               =    -257.98;
SET @TaurenStartZ                                               =    52.9968;
SET @TaurenStartO                                               =          0;

SET @GnomeStartX                                                = @DwarfStartX;
SET @GnomeStartY                                                = @DwarfStartY;
SET @GnomeStartZ                                                = @DwarfStartZ;
SET @GnomeStartO                                                = @DwarfStartO;

SET @TrollStartX                                                = @OrcStartX;
SET @TrollStartY                                                = @OrcStartY;
SET @TrollStartZ                                                = @OrcStartZ;
SET @TrollStartO                                                = @OrcStartO;

SET @BloodElfStartX                                             =    10349.6;
SET @BloodElfStartY                                             =   -6357.29;
SET @BloodElfStartZ                                             =    33.4026;
SET @BloodElfStartO                                             =    5.31605;

SET @DraeneiStartX                                              =   -3961.64;
SET @DraeneiStartY                                              =   -13931.2;
SET @DraeneiStartZ                                              =    100.615;
SET @DraeneiStartO                                              =    2.08364;

SET @DKStartX                                                   =    2358.44;
SET @DKStartY                                                   =    -5666.9;
SET @DKStartZ                                                   =    426.023;
SET @DKStartO                                                   =    3.65997;

-- TaxiNodes
SET @TaxiNodeAuberdine                                         =         26;
SET @TaxiNodeExodar                                            =         94;

-- New TaxiPathNodes
SET @TaxiPathID                          =   (SELECT COALESCE(MAX(id), 0) FROM `dbc_db`.`taxipath`);
SET @TaxiAuberdineExodar             := @TaxiPathID             := @TaxiPathID +1;
SET @TaxiExodarAuberdine             := @TaxiPathID             := @TaxiPathID +1;

-- Talents
SET @MageFire                                                  =        41;
SET @MageFrost                                                 =        61;
SET @MageArcane                                                =        81;
SET @WarriorArms                                               =       161;
SET @WarriorProtection                                         =       163;
SET @WarriorFury                                               =       164;
SET @RogueCombat                                               =       181;
SET @RogueAssassination                                        =       182;
SET @RogueSubtlety                                             =       183;
SET @PriestDiscipline                                          =       201;
SET @PriestHoly                                                =       202;
SET @PriestShadow                                              =       203;
SET @ShamanElementalCombat                                     =       261;
SET @ShamanRestoration                                         =       262;
SET @ShamanEnhancement                                         =       263;
SET @DruidFeralCombat                                          =       281;
SET @DruidRestoration                                          =       282;
SET @DruidBalance                                              =       283;
SET @WarlockDestruction                                        =       301;
SET @WarlockCurses                                             =       302;
SET @WarlockDemonology                                         =       303;
SET @HunterBeastMastery                                        =       361;
SET @HunterSurvival                                            =       362;
SET @HunterMarksmanship                                        =       363;
SET @PaladinRetribution                                        =       381;
SET @PaladinHoly                                               =       382;
SET @PaladinProtection                                         =       383;
SET @DKBlood                                                   =       398;
SET @DKFrost                                                   =       399;
SET @DKUnholy                                                  =       400;
SET @HunterPetTenacity                                         =       409;
SET @HunterPetFerocity                                         =       410;
SET @HunterPetCunning                                          =       411;

-- Other Factions
SET @FactionCreature                                           =         7;
SET @FactionMonster                                            =        14;
SET @FactionDefiasBrotherhood                                  =        15;
SET @FactionGnollRiverpaw                                      =        16;
SET @FactionGnollRedridge                                      =        17;
SET @FactionGnollShadowhide                                    =        18;
SET @FactionMurloc                                             =        19;
SET @FactionScourge                                            =        20;
SET @FactionBootyBay                                           =        21;
SET @FactionBeastSpider                                        =        22;
SET @FactionBeastBoar                                          =        23;
SET @FactionEnemyWorgen                                        =        24;
SET @FactionKobold                                             =        25;
SET @FactionTrollBloodscalp                                    =        26;
SET @FactionTrollSkullsplitter                                 =        27;
SET @FactionPrey                                               =        28;
SET @FactionBeastWolf                                          =        29;
SET @FactionDefiasBrotherhoodTraitor                           =        30;
SET @FactionFriendly                                           =        31;
SET @FactionTrogg                                              =        32;
SET @FactionTrollFrostmane                                     =        33;
SET @FactionOrcBlackrock                                       =        34;
SET @FactionVillian                                            =        35;
SET @FactionVictim                                             =        36;
SET @FactionBeastBear                                          =        37;
SET @FactionOgre                                               =        38;
SET @FactionKurzensMercenaries                                 =        39;
SET @FactionEscortee                                           =        40;
SET @FactionVentureCompany                                     =        41;
SET @FactionBeastRaptor                                        =        42;
SET @FactionBasilisk                                           =        43;
SET @FactionDragonflightGreen                                  =        44;
SET @FactionLostOnes                                           =        45;
SET @FactionBlacksmithingArmorsmithing                         =        46;
SET @FactionIronforge                                          =        47;
SET @FactionDarkIronDwarves                                    =        48;
SET @FactionHumanNightWatch                                    =        49;
SET @FactionDragonflightRed                                    =        50;
SET @FactionGnollMosshide                                      =        51;
SET @FactionOrcDragonmaw                                       =        52;
SET @FactionGnomeLeper                                         =        53;
SET @FactionGnomereganExiles                                   =        54;
SET @FactionLeopard                                            =        55;
SET @FactionScarletCrusade                                     =        56;
SET @FactionGnollRothide                                       =        57;
SET @FactionBeastGorilla                                       =        58;
SET @FactionThoriumBrotherhood                                 =        59;
SET @FactionNaga                                               =        60;
SET @FactionDalaran                                            =        61;
SET @FactionForlornSpirit                                      =        62;
SET @FactionDarkhowl                                           =        63;
SET @FactionGrell                                              =        64;
SET @FactionFurbolg                                            =        65;
SET @FactionHordeGeneric                                       =        66;
SET @FactionHorde                                              =        67;
SET @FactionUndercity                                          =        68;
SET @FactionDarnassus                                          =        69;
SET @FactionSyndicate                                          =        70;
SET @FactionHillsbradMilitia                                   =        71;
SET @FactionStormwind                                          =        72;
SET @FactionDemon                                              =        73;
SET @FactionElemental                                          =        74;
SET @FactionSpirit                                             =        75;
SET @FactionOrgrimmar                                          =        76;
SET @FactionTreasure                                           =        77;
SET @FactionGnollMudsnout                                      =        78;
SET @FactionHIllsbradSouthshoreMayor                           =        79;
SET @FactionDragonflightBlack                                  =        80;
SET @FactionThunderBluff                                       =        81;
SET @FactionTrollWitherbark                                    =        82;
SET @FactionLeatherworkingElemental                            =        83;
SET @FactionQuilboarRazormane                                  =        84;
SET @FactionQuilboarBristleback                                =        85;
SET @FactionLeatherworkingDragonscale                          =        86;
SET @FactionBloodsailBuccaneers                                =        87;
SET @FactionBlackfathom                                        =        88;
SET @FactionMakrura                                            =        89;
SET @FactionCentaurKolkar                                      =        90;
SET @FactionCentaurGalak                                       =        91;
SET @FactionGelkisClanCentaur                                  =        92;
SET @FactionMagramClanCentaur                                  =        93;
SET @FactionMaraudine                                          =        94;
SET @FactionTheramore                                          =       108;
SET @FactionQuilboarRazorfen                                   =       109;
SET @FactionQuilboarRazormane2                                 =       110;
SET @FactionQuilboarDeathshead                                 =       111;
SET @FactionEnemy                                              =       128;
SET @FactionAmbient                                            =       148;
SET @FactionNethergardeCaravan                                 =       168;
SET @FactionSteamwheedleCartel                                 =       169;
SET @FactionAllianceGeneric                                    =       189;
SET @FactionNethergarde                                        =       209;
SET @FactionWailingCaverns                                     =       229;
SET @FactionSilithid                                           =       249;
SET @FactionSilvermoonRemnant                                  =       269;
SET @FactionZandalarTribe                                      =       270;
SET @FactionBlacksmithingWeaponsmithing                        =       289;
SET @FactionScorpid                                            =       309;
SET @FactionBeastBat                                           =       310;
SET @FactionTitan                                              =       311;
SET @FactionTaskmasterFizzule                                  =       329;
SET @FactionRavenholdt                                         =       349;
SET @FactionGadgetzan                                          =       369;
SET @FactionGnomereganBug                                      =       389;
SET @FactionHarpy                                              =       409;
SET @FactionBurningBlade                                       =       429;
SET @FactionShadowsilkPoacher                                  =       449;
SET @FactionSearingSpider                                      =       450;
SET @FactionAlliance                                           =       469;
SET @FactionRatchet                                            =       470;
SET @FactionWildhammerClan                                     =       471;
SET @FactionGoblinDarkIronBarPatron                            =       489;
SET @FactionTheLeagueofArathor                                 =       509;
SET @FactionTheDefilers                                        =       510;
SET @FactionGiant                                              =       511;
SET @FactionArgentDawn                                         =       529;
SET @FactionDarkspearTrolls                                    =       530;
SET @FactionDragonflightBronze                                 =       531;
SET @FactionDragonflightBlue                                   =       532;
SET @FactionLeatherworkingTribal                               =       549;
SET @FactionEngineeringGoblin                                  =       550;
SET @FactionEngineeringGnome                                   =       551;
SET @FactionBlacksmithingHammersmithing                        =       569;
SET @FactionBlacksmithingAxesmithing                           =       570;
SET @FactionBlacksmithingSwordsmithing                         =       571;
SET @FactionTrollVilebranch                                    =       572;
SET @FactionSouthseaFreebooters                                =       573;
SET @FactionCaerDarrow                                         =       574;
SET @FactionFurbolgUncorrupted                                 =       575;
SET @FactionTimbermawHold                                      =       576;
SET @FactionEverlook                                           =       577;
SET @FactionWintersaberTrainers                                =       589;
SET @FactionCenarionCircle                                     =       609;
SET @FactionShatterspearTrolls                                 =       629;
SET @FactionRavasaurTrainers                                   =       630;
SET @FactionMajordomoExecutus                                  =       649;
SET @FactionBeastCarrionBird                                   =       669;
SET @FactionBeastCat                                           =       670;
SET @FactionBeastCrab                                          =       671;
SET @FactionBeastCrocilisk                                     =       672;
SET @FactionBeastHyena                                         =       673;
SET @FactionBeastOwl                                           =       674;
SET @FactionBeastScorpid                                       =       675;
SET @FactionBeastTallstrider                                   =       676;
SET @FactionBeastTurtle                                        =       677;
SET @FactionBeastWindSerpent                                   =       678;
SET @FactionTrainingDummy                                      =       679;
SET @FactionDragonflightBlackBait                              =       689;
SET @FactionBattlegroundNeutral                                =       709;
SET @FactionFrostwolfClan                                      =       729;
SET @FactionStormpikeGuard                                     =       730;
SET @FactionHydraxianWaterlords                                =       749;
SET @FactionSulfuronFirelords                                  =       750;
SET @FactionGizlocksDummy                                      =       769;
SET @FactionGizlocksCharm                                      =       770;
SET @FactionGizlock                                            =       771;
SET @FactionMorogai                                            =       789;
SET @FactionSpiritGuideAlliance                                =       790;
SET @FactionShendralar                                         =       809;
SET @FactionOgreCaptainKromcrush                               =       829;
SET @FactionSpiritGuideHorde                                   =       849;
SET @FactionJaedenar                                           =       869;
SET @FactionWarsongOutriders                                   =       889;
SET @FactionSilverwingSentinels                                =       890;
SET @FactionAllianceForces                                     =       891;
SET @FactionHordeForces                                        =       892;
SET @FactionRevantuskTrolls                                    =       893;
SET @FactionDarkmoonFaire                                      =       909;
SET @FactionBroodofNozdormu                                    =       910;
SET @FactionSilvermoonCity                                     =       911;
SET @FactionMightofKalimdor                                    =       912;
SET @FactionPLAYERBloodElf                                     =       914;
SET @FactionArmiesofCThun                                      =       915;
SET @FactionSilithidAttackers                                  =       916;
SET @FactionTheIronforgeBrigade                                =       917;
SET @FactionRCEnemies                                          =       918;
SET @FactionRCObjects                                          =       919;
SET @FactionRed                                                =       920;
SET @FactionBlue                                               =       921;
SET @FactionTranquillien                                       =       922;
SET @FactionFarstriders                                        =       923;
SET @FactionDEPRECATED                                         =       924;
SET @FactionSunstriders                                        =       925;
SET @FactionMagistersGuild                                     =       926;
SET @FactionPLAYERDraenei                                      =       927;
SET @FactionScourgeInvaders                                    =       928;
SET @FactionBloodmaulClan                                      =       929;
SET @FactionExodar                                             =       930;
SET @FactionTestFactionNotARealFaction                         =       931;
SET @FactionTheAldor                                           =       932;
SET @FactionTheConsortium                                      =       933;
SET @FactionTheScryers                                         =       934;
SET @FactionTheShatar                                          =       935;
SET @FactionShattrathCity                                      =       936;
SET @FactionTrollForest                                        =       937;
SET @FactionTheOmenai                                          =       938;
SET @FactionDEPRECATED                                         =       939;
SET @FactionTheSonsofLothar                                    =       940;
SET @FactionTheMaghar                                          =       941;
SET @FactionCenarionExpedition                                 =       942;
SET @FactionFelOrc                                             =       943;
SET @FactionFelOrcGhost                                        =       944;
SET @FactionSonsofLotharGhosts                                 =       945;
SET @FactionHonorHold                                          =       946;
SET @FactionThrallmar                                          =       947;
SET @FactionTestFaction2                                       =       948;
SET @FactionTestFaction1                                       =       949;
SET @FactionToWoWFlag                                          =       950;
SET @FactionToWoWFlagTriggerAllianceDND                        =       951;
SET @FactionTestFaction3                                       =       952;
SET @FactionTestFaction4                                       =       953;
SET @FactionToWoWFlagTriggerHordeDND                           =       954;
SET @FactionBroken                                             =       955;
SET @FactionEthereum                                           =       956;
SET @FactionEarthElemental                                     =       957;
SET @FactionFightingRobots                                     =       958;
SET @FactionActorGood                                          =       959;
SET @FactionActorEvil                                          =       960;
SET @FactionStillpineFurbolg                                   =       961;
SET @FactionCrazedOwlkin                                       =       962;
SET @FactionChessAlliance                                      =       963;
SET @FactionChessHorde                                         =       964;
SET @FactionMonsterSpar                                        =       965;
SET @FactionMonsterSparBuddy                                   =       966;
SET @FactionTheVioletEye                                       =       967;
SET @FactionSunhawks                                           =       968;
SET @FactionHandofArgus                                        =       969;
SET @FactionSporeggar                                          =       970;
SET @FactionFungalGiant                                        =       971;
SET @FactionSporeBat                                           =       972;
SET @FactionMonsterPredator                                    =       973;
SET @FactionMonsterPrey                                        =       974;
SET @FactionVoidAnomaly                                        =       975;
SET @FactionHyjalDefenders                                     =       976;
SET @FactionHyjalInvaders                                      =       977;
SET @FactionKurenai                                            =       978;
SET @FactionEarthenRing                                        =       979;
SET @FactionTheBurningCrusade                                  =       980;
SET @FactionArakkoa                                            =       981;
SET @FactionZangarmarshBannerAlliance                          =       982;
SET @FactionZangarmarshBannerHorde                             =       983;
SET @FactionZangarmarshBannerNeutral                           =       984;
SET @FactionCavernsofTimeThrall                                =       985;
SET @FactionCavernsofTimeDurnholde                             =       986;
SET @FactionCavernsofTimeSouthshoreGuards                      =       987;
SET @FactionShadowCouncilCovert                                =       988;
SET @FactionKeepersofTime                                      =       989;
SET @FactionTheScaleoftheSands                                 =       990;
SET @FactionDarkPortalDefenderAlliance                         =       991;
SET @FactionDarkPortalDefenderHorde                            =       992;
SET @FactionDarkPortalAttackerLegion                           =       993;
SET @FactionInciterTrigger                                     =       994;
SET @FactionInciterTrigger2                                    =       995;
SET @FactionInciterTrigger3                                    =       996;
SET @FactionInciterTrigger4                                    =       997;
SET @FactionInciterTrigger5                                    =       998;
SET @FactionManaCreature                                       =       999;
SET @FactionKhadgarsServant                                    =      1000;
SET @FactionBladespireClan                                     =      1001;
SET @FactionEthereumSparbuddy                                  =      1002;
SET @FactionProtectorate                                       =      1003;
SET @FactionArcaneAnnihilatorDNR                               =      1004;
SET @FactionFriendlyHidden                                     =      1005;
SET @FactionKirinVarDathric                                    =      1006;
SET @FactionKirinVarBelmara                                    =      1007;
SET @FactionKirinVarLuminrath                                  =      1008;
SET @FactionKirinVarCohlien                                    =      1009;
SET @FactionServantofIllidan                                   =      1010;
SET @FactionLowerCity                                          =      1011;
SET @FactionAshtongueDeathsworn                                =      1012;
SET @FactionSpiritsofShadowmoon1                               =      1013;
SET @FactionSpiritsofShadowmoon2                               =      1014;
SET @FactionNetherwing                                         =      1015;
SET @FactionWyrmcult                                           =      1016;
SET @FactionTreant                                             =      1017;
SET @FactionLeotherasDemonI                                    =      1018;
SET @FactionLeotherasDemonII                                   =      1019;
SET @FactionLeotherasDemonIII                                  =      1020;
SET @FactionLeotherasDemonIV                                   =      1021;
SET @FactionLeotherasDemonV                                    =      1022;
SET @FactionAzaloth                                            =      1023;
SET @FactionRockFlayer                                         =      1024;
SET @FactionFlayerHunter                                       =      1025;
SET @FactionShadowmoonShade                                    =      1026;
SET @FactionLegionCommunicator                                 =      1027;
SET @FactionRavenswoodAncients                                 =      1028;
SET @FactionChessFriendlytoAllChess                            =      1029;
SET @FactionBlackTempleGatesIllidari                           =      1030;
SET @FactionShatariSkyguard                                    =      1031;
SET @FactionArea52                                             =      1032;
SET @FactionMaiev                                              =      1033;
SET @FactionSkettisShadowyArakkoa                              =      1034;
SET @FactionSkettisArakkoa                                     =      1035;
SET @FactionDragonmawEnemy                                     =      1036;
SET @FactionAllianceVanguard                                   =      1037;
SET @FactionOgrila                                             =      1038;
SET @FactionRavager                                            =      1039;
SET @FactionFrenzy                                             =      1041;
SET @FactionSkyguardEnemy                                      =      1042;
SET @FactionSkunkPetunia                                       =      1043;
SET @FactionTheramoreDeserter                                  =      1044;
SET @FactionVrykul                                             =      1045;
SET @FactionNorthseaPirates                                    =      1046;
SET @FactionTuskarr                                            =      1047;
SET @FactionTrollAmani                                         =      1049;
SET @FactionValianceExpedition                                 =      1050;
SET @FactionHordeExpedition                                    =      1052;
SET @FactionWestguard                                          =      1053;
SET @FactionSpottedGryphon                                     =      1054;
SET @FactionTamedPlaguehound                                   =      1055;
SET @FactionVrykulAncientSpirit1                               =      1056;
SET @FactionVrykulAncientSpirit2                               =      1057;
SET @FactionVrykulAncientSpirit3                               =      1058;
SET @FactionCTFFlagAlliance                                    =      1059;
SET @FactionVrykul                                             =      1061;
SET @FactionVrykulGladiator                                    =      1062;
SET @FactionValgardeCombatant                                  =      1063;
SET @FactionTheTaunka                                          =      1064;
SET @FactionMonsterZoneForceReaction1                          =      1065;
SET @FactionMonsterZoneForceReaction2                          =      1066;
SET @FactionTheHandofVengeance                                 =      1067;
SET @FactionExplorersLeague                                    =      1068;
SET @FactionRamRacingPowerupDND                                =      1069;
SET @FactionRamRacingTrapDND                                   =      1070;
SET @FactionCraigsSquirrels                                    =      1071;
SET @FactionTheKaluak                                          =      1073;
SET @FactionHolidayWaterBarrel                                 =      1074;
SET @FactionHolidayGeneric                                     =      1075;
SET @FactionIronDwarves                                        =      1076;
SET @FactionShatteredSunOffensive                              =      1077;
SET @FactionFightingVanityPet                                  =      1078;
SET @FactionMurlocWinterfin                                    =      1079;
SET @FactionFriendlyForceReaction                              =      1080;
SET @FactionObjectForceReaction                                =      1081;
SET @FactionVrykulSea                                          =      1084;
SET @FactionWarsongOffensive                                   =      1085;
SET @FactionPoacher                                            =      1086;
SET @FactionHolidayMonster                                     =      1087;
SET @FactionFurbolgRedfang                                     =      1088;
SET @FactionFurbolgFrostpaw                                    =      1089;
SET @FactionKirinTor                                           =      1090;
SET @FactionTheWyrmrestAccord                                  =      1091;
SET @FactionAzjolNerub                                         =      1092;
SET @FactionTheSilverCovenant                                  =      1094;
SET @FactionGrizzlyHillsTrapper                                =      1095;
SET @FactionWrathoftheLichKing                                 =      1097;
SET @FactionKnightsoftheEbonBlade                              =      1098;
SET @FactionWrathgateScourge                                   =      1099;
SET @FactionWrathgateAlliance                                  =      1100;
SET @FactionWrathgateHorde                                     =      1101;
SET @FactionCTFFlagHorde                                       =      1102;
SET @FactionCTFFlagNeutral                                     =      1103;
SET @FactionFrenzyheartTribe                                   =      1104;
SET @FactionTheOracles                                         =      1105;
SET @FactionArgentCrusade                                      =      1106;
SET @FactionTrollDrakkari                                      =      1107;
SET @FactionCoTArthas                                          =      1108;
SET @FactionCoTStratholmeCitizen                               =      1109;
SET @FactionCoTScourge                                         =      1110;
SET @FactionFreya                                              =      1111;
SET @FactionMountTaxiAlliance                                  =      1112;
SET @FactionMountTaxiHorde                                     =      1113;
SET @FactionMountTaxiNeutral                                   =      1114;
SET @FactionElementalWater                                     =      1115;
SET @FactionElementalAir                                       =      1116;
SET @FactionSholazarBasin                                      =      1117;
SET @FactionClassic                                            =      1118;
SET @FactionTheSonsofHodir                                     =      1119;
SET @FactionIronGiants                                         =      1120;
SET @FactionFrostVrykul                                        =      1121;
SET @FactionEarthen                                            =      1122;
SET @FactionMonsterReferee                                     =      1123;
SET @FactionTheSunreavers                                      =      1124;
SET @FactionHyldsmeet                                          =      1125;
SET @FactionTheFrostborn                                       =      1126;
SET @FactionOrgrimmarAlexTest                                  =      1127;
SET @FactionBilgewaterCartel                                   =      1133;
SET @FactionGilneas                                            =      1134;
SET @FactionTranquillienConversion                             =      1136;
SET @FactionWintersaberConversion                              =      1137;
SET @FactionHatesEverything                                    =      1145;
SET @FactionSilverCovenantConversion                           =      1154;
SET @FactionSunreaversConversion                               =      1155;
SET @FactionTheAshenVerdict                                    =      1156;
SET @FactionCTFFlagAlliance2                                   =      1159;
SET @FactionCTFFlagHorde2                                      =      1160;

-- playercreateinfo_action buttons
SET @Row1Button1                                               =         0;
SET @Row1Button2                                               =         1;
SET @Row1Button3                                               =         2;
SET @Row1Button4                                               =         3;
SET @Row1Button5                                               =         4;
SET @Row1Button6                                               =         5;
SET @Row1Button7                                               =         6;
SET @Row1Button8                                               =         7;
SET @Row1Button9                                               =         8;
SET @Row1Button10                                              =         9;
SET @Row1Button11                                              =        10;
SET @Row1Button12                                              =        11;
SET @SpecialAButton1                                           =        72;
SET @SpecialAButton2                                           =        73;
SET @SpecialAButton3                                           =        74;
SET @SpecialAButton4                                           =        75;
SET @SpecialAButton5                                           =        76;
SET @SpecialAButton6                                           =        77;
SET @SpecialAButton7                                           =        78;
SET @SpecialAButton8                                           =        79;
SET @SpecialAButton9                                           =        80;
SET @SpecialAButton10                                          =        81;
SET @SpecialAButton11                                          =        82;
SET @SpecialAButton12                                          =        83;
SET @SpecialBButton1                                           =        84;
SET @SpecialBButton2                                           =        85;
SET @SpecialBButton3                                           =        86;
SET @SpecialBButton4                                           =        87;
SET @SpecialBButton5                                           =        88;
SET @SpecialBButton6                                           =        89;
SET @SpecialBButton7                                           =        90;
SET @SpecialBButton8                                           =        91;
SET @SpecialBButton9                                           =        92;
SET @SpecialBButton10                                          =        93;
SET @SpecialBButton11                                          =        94;
SET @SpecialBButton12                                          =        95;
SET @SpecialCButton1                                           =        96;
SET @SpecialCButton2                                           =        97;
SET @SpecialCButton3                                           =        98;
SET @SpecialCButton4                                           =        99;
SET @SpecialCButton5                                           =       100;
SET @SpecialCButton6                                           =       101;
SET @SpecialCButton7                                           =       102;
SET @SpecialCButton8                                           =       103;
SET @SpecialCButton9                                           =       104;
SET @SpecialCButton10                                          =       105;
SET @SpecialCButton11                                          =       106;
SET @SpecialCButton12                                          =       107;
SET @SpecialDButton1                                           =       108;
SET @SpecialDButton2                                           =       109;
SET @SpecialDButton3                                           =       110;
SET @SpecialDButton4                                           =       111;
SET @SpecialDButton5                                           =       112;
SET @SpecialDButton6                                           =       113;
SET @SpecialDButton7                                           =       114;
SET @SpecialDButton8                                           =       115;
SET @SpecialDButton9                                           =       116;
SET @SpecialDButton10                                          =       117;
SET @SpecialDButton11                                          =       118;
SET @SpecialDButton12                                          =       119;

-- Common Items
SET @ApprenticesPantsItem                                      =      1395;
SET @ApprenticesShirtItem                                      =      6096;
SET @ApprenticesRobeItem2                                      =      6140;
SET @ApprenticesRobeItem2Display                               =     12649;
SET @ThugShirtItem                                             =      2105;
SET @ThugPantsItem                                             =       120;
SET @ThugBootsItem                                             =       121;
SET @CrudeThrowingAxeItem                                      =     25861;
SET @WornDaggerItem                                            =      2092;
SET @SquiresShirtItem2                                         =      6117; -- dwarf paladin
SET @SquiresPantsItem2                                         =      6118; -- dwarf paladin
SET @SquiresShirtItem3                                         =     23476; -- draenei paladin
SET @SquiresPantsItem3                                         =     23477; -- draenei paladin
SET @LightQuiverItem                                           =      2101;
SET @WornShortbowItem                                          =      2504;
SET @RoughArrowItem                                            =      2512;
SET @WeatheredCrossbowItem                                     =     23347;

SET @BentStaffItem                                             =        35;
SET @WornMaceItem                                              =        36;
SET @WornAxeItem                                               =        37;
SET @SquiresBootsItem                                          =        43;
SET @SquiresPantsItem                                          =        44;
SET @SquiresShirtItem                                          =        45;
SET @NeophytesBootsItem                                        =        51;
SET @NeophytesPantsItem                                        =        52;
SET @NeophytesShirtItem                                        =        53;
SET @ApprenticesBootsItem                                      =        55;
SET @ApprenticesRobeItem                                       =        56;
SET @AcolytesRobeItem                                          =        57;
SET @AcolytesRobeItem2                                         =      6129;
SET @AcolytesShoesItem                                         =        59;
SET @AcolytesPantsItem                                         =      1396;
SET @AcolytesShirtItem                                         =      6097;
SET @RuggedTrappersBootsItem                                   =       129;
SET @RuggedTrappersPantsItem                                   =       147;
SET @RuggedTrappersShirtItem                                   =       148;
SET @PrimitiveKiltItem                                         =       153;
SET @PrimitiveMantleItem                                       =       154;
SET @BattlewornBludgeonItem                                    =      2361;
SET @WornWoodenShieldItem                                      =      2362;
SET @HandcraftedStaffItem                                      =      3661;
SET @HearthstoneItem                                           =      6948;
SET @OldBlunderbussItem                                        =      2508;
SET @SmallAmmoPouchItem                                        =      2102;
SET @LightShotItem                                             =      2516;
SET @NovicesRobeItem                                           =      6123;
SET @NeophytesRobeItem                                         =      6098;
SET @NeophytesRobeItem2                                        =      6144;
SET @NovicesPantsItem                                          =      6124;
SET @NovicesRobeItem2                                          =      6139;
SET @WornBattleaxeItem                                         =     12282;
SET @BattlewornClaymoreItem                                    =     23346;
SET @UnadornedChainBootsItem                                   =     20915;
SET @UnadornedChainLeggingsItem                                =     20918;
SET @UnadornedChainVestItem                                    =     20919;
SET @InitiatesShirtItem                                        =     24143; -- blood elf paladin
SET @InitiatesPantsItem                                        =     24145; -- blood elf paladin
SET @InitiatesBootsItem                                        =     24146; -- blood elf paladin
SET @LightThrowingKnifeItem                                    =     28979;
SET @AcherusKnightsHoodItem                                    =     34652;
SET @AcherusKnightsPauldronsItem                               =     34655;
SET @AcherusKnightsShroudItem                                  =     34659;
SET @AcherusKnightsTunicItem                                   =     34650;
SET @AcherusKnightsWristguardItem                              =     34653;
SET @AcherusKnightsGauntletsItem                               =     34649;
SET @AcherusKnightsGirdleItem                                  =     34651;
SET @AcherusKnightsLegplatesItem                               =     34656;
SET @AcherusKnightsGreavesItem                                 =     34648;
SET @ChokerOfDamnationItem                                     =     34657;
SET @PlagueBandItem                                            =     34658;
SET @DeathweaveBagItem                                         =     38145;
SET @CorruptedBandItem                                         =     38147;
SET @BlackMushroomItem                                         =     41751;
SET @ScourgestoneItem                                          =     40582;
SET @WornDirkItem                                              =     50055;

-- Item Display
SET @NeophytesRobeItem2Display                                 =     12680;
SET @NeophytesPantsItemDisplay                                 =      9944;
SET @NeophytesShirtItemDisplay                                 =      9945;
SET @NeophytesBootsItemDisplay                                 =      9946;
SET @NeophytesBootsItemDisplay                                 =      9946;
SET @NeophytesBootsItemDisplay                                 =      9946;
SET @AcolytesRobeItemDisplay                                   =     12645;
SET @AcolytesShirtItemDisplay                                  =      2470;
SET @AcolytesPantsItemDisplay                                  =      3260;
SET @AcolytesShoesItemDisplay                                  =      3261;
SET @ThugShirtItemDisplay                                      =     10005;
SET @ThugPantsItemDisplay                                      =     10006;
SET @ThugBootsItemDisplay                                      =     10008;
SET @AcolytesRobeItem2Display                                  =     12646;
SET @CrudeThrowingAxeItemDisplay                               =     20777;
SET @WornDaggerItemDisplay                                     =      6442;
SET @WornDirkItemDisplay                                       = @WornDaggerItemDisplay;
SET @ApprenticesRobeItemDisplay                                =     12647;
SET @ApprenticesPantsItemDisplay                               =      9924;
SET @ApprenticesBootsItemDisplay                               =      9929;
SET @ApprenticesShirtItemDisplay                               =      2163;
SET @ApprenticesRobeItemDisplay                                =     12647;
SET @SquiresShirtItem2Display                                  =      9972; -- dwarf paladin
SET @SquiresPantsItem2Display                                  =      9974; -- dwarf paladin
SET @SquiresShirtItem3Display                                  =     36133; -- draenei paladin
SET @SquiresPantsItem3Display                                  =     36134; -- draenei paladin
SET @InitiatesShirtItemDisplay                                 =     36789;
SET @InitiatesPantsItemDisplay                                 =     36790;
SET @InitiatesBootsItemDisplay                                 =     36793;
SET @LightQuiverItemDisplay                                    =     21328;
SET @WornShortbowItemDisplay                                   =      8106;
SET @RoughArrowItemDisplay                                     =      5996;
SET @WeatheredCrossbowItemDisplay                              =     10671;

SET @UnadornedChainBootsItemDisplay                            =     33270;
SET @UnadornedChainLeggingsItemDisplay                         =     33263;
SET @UnadornedChainVestItemDisplay                             =     33268;
SET @BentStaffItemDisplay                                      =       472;
SET @LargeRucksackItemDisplay                                  =       933;
SET @OverseersRingItemDisplay                                  =       963;
SET @SmallAmmoPouchItemDisplay                                 =      1816;
SET @BattlewornClaymoreItemDisplay                             =      2380;
SET @1HDaggerItemDisplay                                       =      2704; -- ?
SET @SquiresShirtItemDisplay                                   =      3265;
SET @WornMaceItemDisplay                                       =      5194;
SET @LightShotItemDisplay                                      =      5998;
SET @HearthstoneItemDisplay                                    =      6418;
SET @GlowingGreenTalismanItemDisplay                           =      6539;
SET @2HRifleItemDisplay                                        =      2409; -- ?
SET @OldBlunderbussItemDisplay                                 =      6606;
SET @2HMaceItemDisplay                                         =      8688; -- ?
SET @BattlewornBludgeonItemDisplay                             =      8690;
SET @SquiresPantsItemDisplay                                   =      9937;
SET @SquiresBootsItemDisplay                                   =      9938;
SET @RuggedTrappersPantsItemDisplay                            =      9975;
SET @RuggedTrappersShirtItemDisplay                            =      9976;
SET @RuggedTrappersBootsItemDisplay                            =      9977;
SET @NovicesPantsItemDisplay                                   =      9987;
SET @PrimitiveKiltItemDisplay                                  =     10050;
SET @PrimitiveMantleItemDisplay                                =     10058;
SET @WornAxeItemDisplay                                        =     14029;
SET @HandcraftedStaffItemDisplay                               =     18530;
SET @NovicesRobeItemDisplay                                    =     12683;
SET @NovicesRobeItemDisplay2                                   =     12684;
SET @WornWoodenShieldItemDisplay                               =     18730;
SET @WornBattleaxeItemDisplay                                  =     22291;
SET @FelConeFungusItemDisplay                                  =     24043;
SET @LightThrowingKnifeItemDisplay                             =     40187;
SET @AcherusKnightsHoodItemDisplay                             =     51495;
SET @AcherusKnightsPauldronsItemDisplay                        =     51501;
SET @AcherusKnightsShroudItemDisplay                           =     49738;
SET @AcherusKnightsTunicItemDisplay                            =     51494;
SET @AcherusKnightsWristguardItemDisplay                       =     51500;
SET @AcherusKnightsGauntletsItemDisplay                        =     51498;
SET @AcherusKnightsGirdleItemDisplay                           =     51497;
SET @AcherusKnightsLegplatesItemDisplay                        =     51499;
SET @AcherusKnightsGreavesItemDisplay                          =     51496;
SET @ChokerOfDamnationItemDisplay                              = @GlowingGreenTalismanItemDisplay;
SET @PlagueBandItemDisplay                                     = @OverseersRingItemDisplay;
SET @DeathweaveBagItemDisplay                                  = @LargeRucksackItemDisplay;
SET @CorruptedBandItemDisplay                                  = @OverseersRingItemDisplay;
SET @BlackMushroomItemDisplay                                  = @FelConeFungusItemDisplay;
SET @ScourgestoneItemDisplay                                   = @HearthstoneItemDisplay;

-- Other Items
SET @GoblinBrawlersHarnessItem                                 =     49524; -- Cataclysm ID
SET @GoblinBrawlersBootsItem                                   =     49527; -- Cataclysm ID
SET @GoblinBrawlersGreavesItem                                 =     49528; -- Cataclysm ID
SET @GoblinBrawlersGauntletsItem                               =     49529; -- Cataclysm ID
SET @GoblinTrappersShirtItem                                   =     49502; -- Cataclysm ID
SET @GoblinTrappersPantsItem                                   =     49503; -- Cataclysm ID
SET @GoblinTrappersBootsItem                                   =     49504; -- Cataclysm ID
SET @WornWoodChopperItem                                       =     52532; -- Cataclysm ID
SET @GoblinThugsTunicItem                                      =     49514; -- Cataclysm ID
SET @GoblinThugsPantsItem                                      =     49515; -- Cataclysm ID
SET @GoblinThugsBootsItem                                      =     49516; -- Cataclysm ID
SET @GoblinNeophytesRobeItem                                   =     49510; -- Cataclysm ID
SET @GoblinNeophytesPantsItem                                  =     49512; -- Cataclysm ID
SET @GoblinNeophytesShoesItem                                  =     49531; -- Cataclysm ID
SET @PrimalShirtItem                                           =     52550; -- Cataclysm ID
SET @PrimalPantsItem                                           =     52551; -- Cataclysm ID
SET @PrimalBootsItem                                           =     52552; -- Cataclysm ID
SET @GoblinApprenticesRobeItem                                 =     49505; -- Cataclysm ID
SET @GoblinApprenticesPantsItem                                =     49506; -- Cataclysm ID
SET @GoblinApprenticesBootsItem                                =     49508; -- Cataclysm ID
SET @GoblinAcolytesRobeItem                                    =     49520; -- Cataclysm ID
SET @GoblinAcolytesPantsItem                                   =     49521; -- Cataclysm ID
SET @GoblinAcolytesShoesItem                                   =     49522; -- Cataclysm ID
SET @GilneanApprenticesRobeItem                                =     49399; -- Cataclysm ID
SET @GilneanApprenticesPantsItem                               =     49400; -- Cataclysm ID
SET @GilneanApprenticesBootsItem                               =     49401; -- Cataclysm ID
SET @GilneanNeophytesRobeItem                                  =     49403; -- Cataclysm ID
SET @GilneanNeophytesPantsItem                                 =     49404; -- Cataclysm ID
SET @GilneanNeophytesBootsItem                                 =     49406; -- Cataclysm ID
SET @GilneanAcolytesRobeItem                                   =     49408; -- Cataclysm ID
SET @GilneanAcolytesPantsItem                                  =     49409; -- Cataclysm ID
SET @GilneanAcolytesBootsItem                                  =     49407; -- Cataclysm ID
SET @GilneanNovicesTunicItem                                   =     49563; -- Cataclysm ID
SET @GilneanNovicesPantsItem                                   =     49566; -- Cataclysm ID
SET @GilneanNovicesBootsItem                                   =     49564; -- Cataclysm ID
SET @GilneanNovicesGlovesItem                                  =     49565; -- Cataclysm ID
SET @GilneanAdventurersShirtItem                               =     49567; -- Cataclysm ID
SET @GilneanTrappersTunicItem                                  =     49570; -- Cataclysm ID
SET @GilneanTrappersShirtItem                                  =     49568; -- Cataclysm ID
SET @GilneanFootpadsPantsItem                                  =     49572; -- Cataclysm ID
SET @GilneanTrappersBootsItem                                  =     49569; -- Cataclysm ID
SET @GilneanTrappersGlovesItem                                 =     49571; -- Cataclysm ID
SET @GilneanFootpadsTunicItem                                  =     49574; -- Cataclysm ID
SET @GilneanFootpadsBootsItem                                  =     49575; -- Cataclysm ID
SET @GilneanFootpadsGlovesItem                                 =     49573; -- Cataclysm ID
SET @GilneanRecruitsTunicItem                                  =     49578; -- Cataclysm ID
SET @GilneanRecruitsPantsItem                                  =     49576; -- Cataclysm ID
SET @GilneanRecruitsBootsItem                                  =     49579; -- Cataclysm ID
SET @GilneanRecruitsBeltItem                                   =     49577; -- Cataclysm ID
SET @WornWoodChopperItem                                       =     52532; -- Cataclysm ID

-- ItemDisplay
SET @GoblinBrawlersGreavesItemDisplay                          =     69183; -- Cataclysm ID?
SET @GoblinBrawlersHarnessItemDisplay                          =     69181; -- Cataclysm ID?
SET @GoblinBrawlersBootsItemDisplay                            =     69185; -- Cataclysm ID?
SET @GoblinBrawlersGauntletsItemDisplay                        =     69182; -- Cataclysm ID?
SET @GoblinTrappersShirtItemDisplay                            =     62614; -- Cataclysm ID?
SET @GoblinTrappersPantsItemDisplay                            =     69187; -- Cataclysm ID?
SET @GoblinTrappersBootsItemDisplay                            =     62617; -- Cataclysm ID?
SET @WornWoodChopperItemDisplay                                =     65743; -- Cataclysm ID?
SET @GoblinThugsTunicItemDisplay                               =     65799; -- Cataclysm ID?
SET @GoblinThugsPantsItemDisplay                               =     69188; -- Cataclysm ID?
SET @GoblinThugsBootsItemDisplay                               =     65798; -- Cataclysm ID?
SET @GoblinNeophytesRobeItemDisplay                            =     65789; -- Cataclysm ID?
SET @GoblinNeophytesPantsItemDisplay                           =     62598; -- Cataclysm ID?
SET @GoblinNeophytesShoesItemDisplay                           =      6318; -- Cataclysm ID?
SET @PrimalShirtItemDisplay                                    =     65801; -- Cataclysm ID?
SET @PrimalPantsItemDisplay                                    =     62573; -- Cataclysm ID?
SET @PrimalBootsItemDisplay                                    =     65800; -- Cataclysm ID?
SET @GoblinApprenticesRobeItemDisplay                          =     62618; -- Cataclysm ID?
SET @GoblinApprenticesPantsItemDisplay                         =     62621; -- Cataclysm ID?
SET @GoblinApprenticesBootsItemDisplay                         = @ApprenticesBootsItemDisplay;
SET @GoblinAcolytesRobeItemDisplay                             =     65787; -- Cataclysm ID?
SET @GoblinAcolytesPantsItemDisplay                            = @GoblinApprenticesPantsItemDisplay;
SET @GoblinAcolytesShoesItemDisplay                            =      4143; -- Cataclysm ID?
SET @GilneanApprenticesRobeItemDisplay                         =     62549; -- Cataclysm ID?
SET @GilneanApprenticesPantsItemDisplay                        =     62561; -- Cataclysm ID?
SET @GilneanApprenticesBootsItemDisplay                        =     62448; -- Cataclysm ID?
SET @GilneanNeophytesRobeItemDisplay                           =     62557; -- Cataclysm ID?
SET @GilneanNeophytesPantsItemDisplay                          =     62559; -- Cataclysm ID?
SET @GilneanNeophytesBootsItemDisplay                          =     62568; -- Cataclysm ID?
SET @GilneanAcolytesBootsItemDisplay                           =     68132; -- Cataclysm ID?
SET @GilneanAcolytesRobeItemDisplay                            =     62565; -- Cataclysm ID?
SET @GilneanAcolytesPantsItemDisplay                           =     62566; -- Cataclysm ID?
SET @GilneanNovicesTunicItemDisplay                            =     65854; -- Cataclysm ID?
SET @GilneanNovicesBootsItemDisplay                            =     65851; -- Cataclysm ID?
SET @GilneanNovicesGlovesItemDisplay                           =     65852; -- Cataclysm ID?
SET @GilneanNovicesPantsItemDisplay                            =     65853; -- Cataclysm ID?
SET @GilneanAdventurersShirtItemDisplay                        =     62558; -- Cataclysm ID?
SET @GilneanTrappersShirtItemDisplay                           =     62706; -- Cataclysm ID?
SET @GilneanTrappersBootsItemDisplay                           =     62707; -- Cataclysm ID?
SET @GilneanTrappersTunicItemDisplay                           =     98023; -- Cataclysm ID?
SET @GilneanTrappersGlovesItemDisplay                          =     69176; -- Cataclysm ID?
SET @GilneanFootpadsPantsItemDisplay                           =     65849; -- Cataclysm ID?
SET @GilneanFootpadsGlovesItemDisplay                          =     69175; -- Cataclysm ID?
SET @GilneanFootpadsTunicItemDisplay                           =     65850; -- Cataclysm ID?
SET @GilneanFootpadsBootsItemDisplay                           =     65847; -- Cataclysm ID?
SET @GilneanRecruitsPantsItemDisplay                           =     68130; -- Cataclysm ID?
SET @GilneanRecruitsBeltItemDisplay                            =     68129; -- Cataclysm ID?
SET @GilneanRecruitsTunicItemDisplay                           =     68128; -- Cataclysm ID?
SET @GilneanRecruitsBootsItemDisplay                           =     68131; -- Cataclysm ID?
SET @WornWoodChopperItemDisplay                                =     65743; -- Cataclysm ID?

-- Recurring Localizations
SET @RacialNameenUS                                            = 'Racial';
SET @RacialNamekoKR                                            = '종족 특성';
SET @RacialNamefrFR                                            = 'Raciale';
SET @RacialNamedeDE                                            = 'Volksfähigkeit';
SET @RacialNamezhCN                                            = '种族特长';
SET @RacialNamezhTW                                            = '種族特長';
SET @RacialNameesES                                            = 'Racial';
SET @RacialNameesMX                                            = 'Racial';
SET @RacialNameruRU                                            = 'Расовая';
SET @RacialNamejaJP                                            =  '';
SET @RacialNameptPT                                            =  '';
SET @RacialNameitIT                                            =  '';

SET @RacialPassiveNameenUS                                     = 'Racial Passive';
SET @RacialPassiveNamekoKR                                     = '종족 지속효과';
SET @RacialPassiveNamefrFR                                     = 'Raciale passive';
SET @RacialPassiveNamedeDE                                     = 'Passive Volksfähigkeit';
SET @RacialPassiveNamezhCN                                     = '被动种族特长';
SET @RacialPassiveNamezhTW                                     = '種族特長，被動';
SET @RacialPassiveNameesES                                     = 'Pasivo racial';
SET @RacialPassiveNameesMX                                     = 'Pasivo racial';
SET @RacialPassiveNameruRU                                     = 'Расовая, пассивная';
SET @RacialPassiveNamejaJP                                     =  '';
SET @RacialPassiveNameptPT                                     =  '';
SET @RacialPassiveNameitIT                                     =  '';

-- Spell Attributes
SET @SPELL_ATTR0_IS_ABILITY                                    =         16;
SET @SPELL_ATTR0_PASSIVE                                       =         64;
SET @SPELL_ATTR0_DO_NOT_DISPLAY_SPELLBOOK_AURA_ICON_COMBAT_LOG =        128;
SET @SPELL_ATTR0_DO_NOT_LOG                                    =        256;
SET @SPELL_ATTR0_ON_NEXT_SWING                                 =       1024;
SET @SPELL_ATTR0_OUTDOORS_ONLY                                 =      32768;
SET @SPELL_ATTR0_NOT_SHAPESHIFTED                              =      65536;
SET @SPELL_ATTR0_DO_NOT_SHEATH                                 =     262144;
SET @SPELL_ATTR0_CANCELS_AUTO_ATTACK_COMBAT                    =    1048576;
SET @SPELL_ATTR0_ALLOW_WHILE_MOUNTED                           =   16777216;
SET @SPELL_ATTR0_ALLOW_WHILE_SITTING                           =  134217728;
SET @SPELL_ATTR0_NOT_IN_COMBAT_ONLY_PEACEFUL                   =  268435456;
SET @SPELL_ATTR0_NO_IMMUNITIES                                 =  536870912;

SET @SPELL_ATTR2_NO_SCHOOL_IMMUNITIES                          =   67108864;

SET @SPELL_ATTR1_NO_REDIRECTION                                =          8;
SET @SPELL_ATTR1_ALLOW_WHILE_STEALTHED                         =         32;
SET @SPELL_ATTR1_NO_REFLECTION                                 =        128;
SET @SPELL_ATTR1_NO_THREAT                                     =       1024;
SET @SPELL_ATTR1_NO_AURA_ICON                                  =  268435456;
SET @SPELL_ATTR1_CAST_WHEN_LEARNED                             = 2147483648;
SET @SPELL_ATTR3_ALLOW_AURA_WHILE_DEAD                         =    1048576;
SET @SPELL_ATTR3_IGNORE_CASTER_AND_TARGET_RESTRICTIONS         =  268435456;
SET @SPELL_ATTR3_IGNORE_CASTER_MODIFIERS                       =  536870912;

SET @SPELL_ATTR3_SUPPRESS_CASTER_PROCS                         =      65536;
SET @SPELL_ATTR3_DO_NOT_DISPLAY_RANGE                          = 1073741824;


SET @SPELL_ATTR4_FORCE_DISPLAY_CASTBAR                         =  134217728;

SET @SPELL_ATTR6_ALLOW_WHILE_RIDING_VEHICLE                    =       4096;
SET @SPELL_ATTR6_ALLOW_EQUIP_WHILE_CASTING                     =     131072;

-- skillraceclassinfo: 0 inserts, 104 updates, 0 deletes

-- Changed values
-- Maybe this is sufficient?
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `race_mask` & @BaseAllianceMask;
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @HordeMask WHERE `race_mask` & @BaseHordeMask;

-- Alliance
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` IN (
    @CommonSkillRaceClassAlliance, -- Skill 98: Language: Common [Alliance]
    @OrcishSkillRaceClassAlliance -- Skill 109: Language: Orcish [Alliance]
);

-- Horde
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @HordeMask    WHERE `id` IN (
    @OrcishSkillRaceClassHorde, -- Skill 109: Language: Orcish [Horde]
    @CommonSkillRaceClassHorde -- Skill 98: Language: Common [Horde]
);

-- Everyone
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask WHERE `id` IN (
    @LeatherworkingSkillRaceClass, -- Skill 165: Leatherworking
    @PlateMailSkillRaceClass, -- Skill 293: Plate Mail
    @PlateMailDKSkillRaceClass, -- Skill 293: Plate Mail
    @FishingSkillRaceClass, -- Skill 356: Fishing
    @HerbalismSkillRaceClass, -- Skill 182: Herbalism
    @MiningSkillRaceClass, -- Skill 186: Mining
    @SkinningSkillRaceClass, -- Skill 393: Skinning
    @DemonTongueSkillRaceClass, -- Skill 139: Language: Demon Tongue
    @DraconicSkillRaceClass, -- Skill 138: Language: Draconic
    @OldTongueSkillRaceClass, -- Skill 141: Language: Old Tongue
    @TitanSkillRaceClass, -- Skill 140: Language: Titan
    @GunsNonHunterSkillRaceClass, -- Skill 46: Guns
    @Mail40SkillRaceClass, -- Skill 413: Mail
    @MailSkillRaceClass, -- Skill 413: Mail
    @LeatherSkillRaceClass, -- Skill 414: Leather
    @ClothSkillRaceClass, -- Skill 415: Cloth
    @AlchemySkillRaceClass, -- Skill 171: Alchemy
    @BlacksmithingSkillRaceClass, -- Skill 164: Blacksmithing
    @EngineeringSkillRaceClass, -- Skill 202: Engineering
    @ShieldSkillRaceClass, -- Skill 433: Shield
    @EnchantingSkillRaceClass, -- Skill 333: Enchanting
    @CookingSkillRaceClass, -- Skill 185: Cooking
    @TailoringSkillRaceClass, -- Skill 197: Tailoring
    @FistWeaponsSkillRaceClass, -- Skill 473: Fist Weapons
    @2HAxePaladinSkillRaceClass, -- Skill 172: Two-Handed Axes
    @2HAxeShamanSkillRaceClass, -- Skill 172: Two-Handed Axes
    @2HAxeDKSkillRaceClass, -- Skill 172: Two-Handed Axes
    @2HAxeHunterSkillRaceClass, -- Skill 172: Two-Handed Axes
    @AxesHunterSkillRaceClass2, -- Skill 44: Axes (this is the one that Blood Elves and Draenei were added to, so I'll add to it as well)
    @AxesWarriorSkillRaceClass2, -- Skill 44: Axes (this is the one that Draenei were added to, so I'll add to it as well)
    @AxesDKSkillRaceClass, -- Skill 44: Axes
    @AxesOtherSkillRaceClass, -- Skill 44: Axes (paladin, rogue, shaman)
    @DaggersHunterSkillRaceClass2, -- Skill 173: Daggers (this is the one that Draenei were added to, so I'll add to it as well)
    @DaggersWarriorSkillRaceClass2, -- Skill 173: Daggers (this is the one that Draenei were added to, so I'll add to it as well)
    @MacesWarriorSkillRaceClass2, -- Skill 54: Maces
    @MacesPaladinSkillRaceClass, -- Skill 54: Maces
    @MacesDKSkillRaceClass, -- Skill 54: Maces
    @MacesPriestShamanSkillRaceClass, -- Skill 54: Maces
    @SurvivalSkillRaceClass, -- Skill 142: Survival
    @JewelcraftingSkillRaceClass, -- Skill 755: Jewelcrafting
    @SwordsPaladinSkillRaceClass, -- Skill 43: Swords
    @SwordsRogueSkillRaceClass, -- Skill 43: Swords
    @SwordsMageWarlockSkillRaceClass, -- Skill 43: Swords
    @DaggersRogueWarlockSkillRaceClass, -- Skill 173: Daggers
    @DaggersCastersSkillRaceClass, -- Skill 173: Daggers
    @SwordsDKSkillRaceClass, -- Skill 43: Swords
    @StavesCastersSkillRaceClass, -- Skill 136: Staves
    @StavesWarriorHunterSkillRaceClass, -- Skill 136: Staves
    @PolearmsSkillRaceClass, -- Skill 229: Polearms
    @PolearmsDKSkillRaceClass, -- Skill 229: Polearms
    @DualWieldRogueSkillRaceClass, -- Skill 118: Dual Wield
    @DualWieldWarriorHunterSkillRaceClass, -- Skill 118: Dual Wield
    @DualWieldShamanSkillRaceClass, -- Skill 118: Dual Wield
    @DualWieldDKSkillRaceClass -- Skill 118: Dual Wield
);

-- Almost every race
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask & ~(@DwarfMask  | @TaurenMask | @TrollMask)   WHERE `id` = @SwordsWarriorSkillRaceClass; -- Skill 43: Swords (the exempt are in 638 for some reason)
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask & ~@DraeneiMask                               WHERE `id` = @SwordsHunterSkillRaceClass; -- Skill 43: Swords (Draenei hunters get this skill in 880 for some reason)
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask & ~@Undead                                    WHERE `id` = @GutterspeakSkillRaceClass; -- Skill 673: Language: Gutterspeak
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask & ~(@OrcMask    | @DwarfMask)                 WHERE `id` = @2HAxeWarriorSkillRaceClass; -- Skill 172: Two-Handed Axes
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask & ~(@TaurenMask | @DraeneiMask)               WHERE `id` = @DaggersDruidNightElfSkillRaceClass; -- Skill 173: Daggers
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask & ~(@TaurenMask | @DraeneiMask)               WHERE `id` = @MacesDruidNightElfSkillRaceClass; -- Skill 54: Maces
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @PlayableRaceMask & ~@TaurenMask                                WHERE `id` = @2HMaceSkillRaceClass2; -- Skill 160: Two-Handed Maces (the other one only has Tauren, so I updated this one)

-- Some races (most are probably redundant)
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @TaurenMask | @DraeneiMask                                                   WHERE `id` = @MacesDruidTaurenSkillRaceClass; -- Skill 54: Maces
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @TaurenMask | @DraeneiMask                                                   WHERE `id` = @DaggersDruidNightElfSkillRaceClass; -- Skill 173: Daggers
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | (@PlayableRaceMask & ~@GunHunters)                                           WHERE `id` = @GunsHunterStartSkillRaceClass; -- Skill 46: Guns
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @GunHunters                                                                  WHERE `id` = @GunsHunterStartSkillRaceClass; -- Skill 46: Guns
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | (@VanillaAllianceMask & ~@HumanMask) | (@VanillaHordeMask & ~@TaurenMask)    WHERE `id` = @HorseRidingGeneralSkillRaceClass; -- Skill 148: Horse Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @VanillaAllianceMask | (@VanillaHordeMask & ~@OrcMask) | @GoblinMask         WHERE `id` = @WolfRidingGeneralSkillRaceClass; -- Skill 149: Wolf Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | (@VanillaAllianceMask & ~@DwarfMask) | (@VanillaHordeMask & ~@TaurenMask)    WHERE `id` = @RamRidingGeneralSkillRaceClass; -- Skill 152: Ram Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | (@VanillaAllianceMask & ~@NightElfMask) | (@VanillaHordeMask & ~@TaurenMask) WHERE `id` = @TigerRidingGeneralSkillRaceClass; -- Skill 150: Tiger Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @VanillaAllianceMask | @OrcMask | @UndeadMask                                WHERE `id` = @UndeadHorsemanshipGeneralSkillRaceClass; -- Skill 554: Undead Horsemanship
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @VanillaAllianceMask | @OrcMask | @UndeadMask                                WHERE `id` = @RaptorRidingGeneralSkillRaceClass; -- Skill 533: Raptor Riding

/*
-- Only one race (probably redundant)
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @HumanMask     WHERE `id` = @HorseRidingHumanSkillRaceClass; -- Skill 148: Horse Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @OrcMask       WHERE `id` = @WolfRidingOrcSkillRaceClass; -- Skill 149: Wolf Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @DwarfMask     WHERE `id` = @RamRidingDwarfSkillRaceClass; -- Skill 152: Ram Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @NightElfMask  WHERE `id` = @TigerRidingNightElfSkillRaceClass; -- Skill 150: Tiger Riding
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @GnomeMask     WHERE `id` = @MechanostriderPilotingGnomeSkillRaceClass; -- Skill 553: Mechanostrider Piloting
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @DwarfMask     WHERE `id` = @MechanostriderPilotingDwarfSkillRaceClass; -- Skill 553: Mechanostrider Piloting

-- Removed skills?
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 24; -- Skill 272: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 26; -- Skill 247: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 34; -- Skill 273: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 35; -- Skill 262: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 36; -- Skill 263: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 37; -- Skill 264: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 38; -- Skill 260: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 54; -- Skill 130: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 59; -- Skill 96: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 62; -- Skill 268: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 64; -- Skill 269: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 65; -- Skill 198: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 66; -- Skill 246: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 73; -- Skill 254: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 76; -- Skill 241: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 79; -- Skill 238: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 81; -- Skill 239: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 83; -- Skill 252: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 97; -- Skill 199: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 104; -- Skill 353: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 105; -- Skill 120: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 106; -- Skill 245: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 108; -- Skill 255: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 111; -- Skill 244: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 112; -- Skill 243: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 113; -- Skill 258: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 137; -- Skill 227: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 149; -- Skill 242: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 151; -- Skill 416: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 155; -- Skill 416: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 158; -- Skill 416: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 159; -- Skill 416: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 175; -- Skill 418: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 178; -- Skill 418: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 183; -- Skill 418: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 186; -- Skill 418: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 189; -- Skill 419: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 191; -- Skill 419: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 193; -- Skill 419: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 198; -- Skill 419: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 200; -- Skill 419: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 203; -- Skill 420: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 204; -- Skill 420: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 205; -- Skill 420: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 265; -- Skill 419: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 266; -- Skill 419: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 268; -- Skill 420: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 269; -- Skill 420: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 270; -- Skill 418: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 271; -- Skill 416: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 272; -- Skill 453: N/A
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AllianceMask WHERE `id` = 403; -- Skill 515: N/A
*/
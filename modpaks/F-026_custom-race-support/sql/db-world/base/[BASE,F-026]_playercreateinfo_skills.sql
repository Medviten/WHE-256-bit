-- Ranged weapons (Hunters)
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @GunHunters,
    `raceMask_2` = `raceMask_2` | @GunHunters_2      WHERE `skill` = @GunSkill;
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @BowHunters,
    `raceMask_2` = `raceMask_2` | @BowHunters_2      WHERE `skill` = @BowSkill;
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @CrossbowHunters,
    `raceMask_2` = `raceMask_2` | @CrossbowHunters_2 WHERE `skill` = @CrossbowSkill;

-- Daggers
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | (@PlayableRaceMask & ~@DaggersRogueOnly),
    `raceMask_2` = `raceMask_2` | (@PlayableRaceMask_2 & ~@DaggersRogueOnly) WHERE `skill` = @DaggerSkill AND (`classMask` & @RogueMask) != 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(0, @RogueMask, @DaggerSkill, 0, 'Daggers (Rogues)');

-- Two-Handed Maces
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @AllianceMask,
    `raceMask_2` = `raceMask_2` | @AllianceMask_2 WHERE `classMask` & @PaladinMask AND `skill` = @2HMaceSkill AND (`classMask` & @PaladinMask) != 0;;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@AllianceMask, @PaladinMask, @2HMaceSkill, 0, '2H-Maces - Alliance Paladins', @AllianceMask_2); -- 2H-Maces

/* Add appropriate languages */
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @AllianceMask,
    `raceMask_2` = `raceMask_2` | @AllianceMask_2 WHERE `skill` = @CommonSkill;
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @HordeMask,
    `raceMask_2` = `raceMask_2` | @HordeMask_2    WHERE `skill` = @OrcishSkill;

-- Ranged weapons (Hunters)
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @GunHunters      WHERE `skill` = @GunSkill;
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @BowHunters      WHERE `skill` = @BowSkill;
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @CrossbowHunters WHERE `skill` = @CrossbowSkill;

-- Daggers
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | (@PlayableRaceMask & ~@DaggersRogueOnly) WHERE `skill` = @DaggerSkill AND (`classMask` & @RogueMask) != 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(0, @RogueMask, @DaggerSkill, 0, 'Daggers (Rogues)');

-- Two-Handed Maces
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @AllianceMask WHERE `classMask` & @PaladinMask AND `skill` = @2HMaceSkill AND (`classMask` & @PaladinMask) != 0;;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@AllianceMask, @PaladinMask, @2HMaceSkill, 0, '2H-Maces - Alliance Paladins'); -- 2H-Maces

/* Add appropriate languages */
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @AllianceMask WHERE `skill` = @CommonSkill;
UPDATE `playercreateinfo_skills` SET `raceMask` = `raceMask` | @HordeMask    WHERE `skill` = @OrcishSkill;

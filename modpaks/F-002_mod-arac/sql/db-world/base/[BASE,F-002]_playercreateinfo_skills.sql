UPDATE `playercreateinfo_skills` SET `raceMask`  = @BowHunters,
    `raceMask_2` = @BowHunters_2                  WHERE `skill` = @BowSkill      AND `classMask`                  != 0;
UPDATE `playercreateinfo_skills` SET `raceMask`  = @GunHunters,
    `raceMask_2` = @GunHunters_2                  WHERE `skill` = @GunSkill      AND `classMask`                  != 0;
UPDATE `playercreateinfo_skills` SET `raceMask`  = @CrossbowHunters,
    `raceMask_2` = @CrossbowHunters_2             WHERE `skill` = @CrossbowSkill AND `classMask`                  != 0;
UPDATE `playercreateinfo_skills` SET `classMask` = `classMask` & ~@RogueMask    WHERE `skill` = @DaggerSkill   AND (`classMask` & @RogueMask)   != 0;
UPDATE `playercreateinfo_skills` SET `classMask` = `classMask` & ~@PaladinMask  WHERE `skill` = @2HMaceSkill   AND (`classMask` & @PaladinMask) != 0;

INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(0,             @RogueMask,   @DaggerSkill, 0, 'Daggers (Rogues)', 0),
(@AllianceMask, @PaladinMask, @2HMaceSkill, 0, '2H-Maces (Alliance Paladins)', @AllianceMask_2);

-- Classic ARAC approach equalizes skills across races instead:
-- UPDATE `playercreateinfo_skills` SET `raceMask` = 0 WHERE `skill` IN (@BowSkill, @GunSkill, @CrossbowSkill, @2HMaceSkill, @DaggerSkill) AND `classMask` != 0;

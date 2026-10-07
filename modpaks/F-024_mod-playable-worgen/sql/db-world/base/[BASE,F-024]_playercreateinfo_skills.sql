/*Updates existing starting skills to include Worgen where relevant
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @WorgenMask WHERE `skill` = @BowSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @WorgenMask WHERE `skill` = @GunSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @WorgenMask WHERE `skill` = @DaggerSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @WorgenMask WHERE `skill` = @2HMaceSkill;

UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @WorgenMask WHERE `skill` = @CommonSkill;
*/

-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @WorgenMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@WorgenMask, 0, @WorgenRacials, 0, 'Worgen - Racial');

/* Grants all newly created worgen rogues the ability to use their starting weapon */
/* Worgen rogues start with an axe, but rogues don't start with the weapon skill learned by default */
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @WorgenMask AND `classMask` = @RogueMask;
INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@WorgenMask, @RogueMask, @AxeSkill, 0, 'Axes - Worgen');
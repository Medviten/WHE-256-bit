-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @GoblinMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@GoblinMask, 0, @GoblinRacials, 0, 'Goblin - Racial');

/* Updates existing starting skills to include Goblins where relevant */
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @GoblinMask WHERE `skill` = @2HMaceSkill;

/* Goblin rogues start with a mace, but rogues don't start with the weapon skill learned by default */
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @GoblinMask AND `classMask` = @RogueMask;
INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@GoblinMask, @RogueMask, @MaceSkill, 0, 'Maces - Goblin');

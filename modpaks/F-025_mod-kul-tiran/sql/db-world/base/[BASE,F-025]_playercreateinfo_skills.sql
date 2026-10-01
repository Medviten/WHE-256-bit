/*
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @KulTiranMask WHERE `skill` = @CrossbowSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @KulTiranMask WHERE `skill` = @DaggerSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @KulTiranMask WHERE `skill` = @2HMaceSkill;

UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @KulTiranMask WHERE `skill` = @CommonSkill;
*/
-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @KulTiranMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@KulTiranMask, 0, @KulTiranRacials, 0, 'Kul Tiran - Racial');
/*Updates existing starting skills to include LightforgedDraenei where relevant
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @LightforgedDraeneiMask WHERE `skill` = @BowSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @LightforgedDraeneiMask WHERE `skill` = @GunSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @LightforgedDraeneiMask WHERE `skill` = @DaggerSkill;
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @LightforgedDraeneiMask WHERE `skill` = @2HMaceSkill;

UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @LightforgedDraeneiMask WHERE `skill` = @CommonSkill;
*/

-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @LightforgedDraeneiMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@LightforgedDraeneiMask, 0, @LightforgedDraeneiRacials, 0, 'LightforgedDraenei - Racial');
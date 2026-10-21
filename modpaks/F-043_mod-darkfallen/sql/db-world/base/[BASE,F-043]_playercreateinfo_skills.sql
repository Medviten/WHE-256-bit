/* Updates existing starting skills to include Darkfallen where relevant */
/* I have commented out Guns for Darkfallen because other Hunters in WotLK start with only one ranged weapon skill. */
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @DarkfallenMask WHERE `skill` = 46; -- Guns
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @DarkfallenMask WHERE `skill` = 45; -- Bows
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @DarkfallenMask WHERE `skill` = 173; -- Daggers

/* Special cases */ 
-- INSERT IGNORE INTO `playercreateinfo_skills` (`racemask`, `classMask`, `skill`, `rank`, `comment`) VALUES
-- (0, @PaladinMask, 160, 0, '2H-Maces - Paladins'); -- 2H-Maces

/* Add appropriate languages to Darkfallen */
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @DarkfallenMask WHERE `skill` = 98; -- Common language
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @DarkfallenMask WHERE `skill` = 137; -- Thalassian language

/* Add racial skills */
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` IN (@DarkfallenMask) AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@DarkfallenMask, 0, @DarkfallenRacials, 0, 'Darkfallen - Racial');

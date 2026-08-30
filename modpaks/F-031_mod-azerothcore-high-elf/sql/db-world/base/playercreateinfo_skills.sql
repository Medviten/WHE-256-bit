/*Updates existing starting skills to include High Elves where relevant*/
/* Only update skill if it has the default racemask to prevent conflict with other modules that change starting weapon skills. */
/* I have commented out Guns for High Elves because other Hunters in WotLK start with only one ranged weapon skill. */
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask`|4096 WHERE `skill` = 46 AND `racemask` = 36; -- Guns
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask`|4096 WHERE `skill` = 45 AND `racemask` = 650; -- Bows
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask`|4096 WHERE `skill` = 173 AND `racemask` = 735; -- Daggers

/* Special cases */ 
INSERT IGNORE INTO `playercreateinfo_skills` (`racemask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(0, 2, 160, 0, '2H-Maces - Paladins'); -- 2H-Maces for all Paladins

/* Add appropriate faction language to Worgen, Goblins, and High Elves */
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask`|4096 WHERE `skill` = 98; -- Common language
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask`|4096 WHERE `skill` = 137; -- Thalassian language

/* Add racial skills */
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` IN (256, 2048, 4096, 8192) AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(4096, 0, 791, 0, 'High Elf - Racial');

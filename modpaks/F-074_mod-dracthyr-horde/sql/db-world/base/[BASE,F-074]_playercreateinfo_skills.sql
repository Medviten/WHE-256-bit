-- Racial skills
-- Race 70 only has a bit in the second mask word. Removes the row older versions wrote without it, which gave every race this skill
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = 0 AND `classMask` = 0 AND `skill` = @HordeDracthyrRacials;
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @HordeDracthyrMask AND `raceMask_2` = @HordeDracthyrMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@HordeDracthyrMask, 0, @HordeDracthyrRacials, 0, @HordeDracthyrRacialNameenUS, @HordeDracthyrMask_2);

-- skillraceclassinfo: Alliance Pandaren can have the racial skill of F-129
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @AlliancePandarenMask,
    `race_mask_2` = `race_mask_2` | @AlliancePandarenMask_2 WHERE `id` = @PandarenRacialSkillRaceClass;

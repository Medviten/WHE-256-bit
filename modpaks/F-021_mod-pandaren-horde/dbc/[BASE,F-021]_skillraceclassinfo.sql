-- skillraceclassinfo: Horde Pandaren can have the racial skill of F-129
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @HordePandarenMask,
    `race_mask_2` = `race_mask_2` | @HordePandarenMask_2 WHERE `id` = @PandarenRacialSkillRaceClass;

-- charhairtextures: 6 inserts, 0 updates, 0 deletes

SET @CharHairTexturesID = (SELECT COALESCE(MAX(id), 0) FROM `charhairtextures`);

-- New entries
DELETE FROM `charhairtextures` WHERE `race` = @HighmountainTauren;
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES
(@CharHairTexturesID := @CharHairTexturesID +1, @HighmountainTauren, @Male,   0, 255, 0, 1, 1),
(@CharHairTexturesID := @CharHairTexturesID +1, @HighmountainTauren, @Female, 0, 255, 0, 1, 1),
(@CharHairTexturesID := @CharHairTexturesID +1, @HighmountainTauren, @Male,   0, 255, 0, 1, 1),
(@CharHairTexturesID := @CharHairTexturesID +1, @HighmountainTauren, @Female, 0, 255, 0, 1, 1);

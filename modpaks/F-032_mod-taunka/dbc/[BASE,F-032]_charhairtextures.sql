-- charhairtextures: 1 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairtextures` WHERE `race` = @Taunka;
SET @CharHairTexturesID = (SELECT COALESCE(MAX(id), 0) FROM `charhairtextures`);
INSERT INTO `charhairtextures` (`id`, `race`, `gender`, `unk_1`, `unk_2`, `unk_3`, `unk_4`, `unk_5`) VALUES
(@CharHairTexturesID := @CharHairTexturesID +1, @Taunka, @Male,   0, 255, -1, 0, 0);

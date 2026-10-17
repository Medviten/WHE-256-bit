-- charhairgeosets: 15 inserts, 0 updates, 0 deletes

-- New entries
-- The "hair" slider picks the horns: retail horn geosets 2401-2404, 2406-2408 (male) / 2401-2408 (female) are
-- renumbered to hair geosets 1-7 / 1-8 in the M2 skins (see tools/patch_eyes/select_geosets.py). The hair colour
-- slider picks the horn colour through CharSections (4 colours, then the same 4 with carved markings).
DELETE FROM `charhairgeosets` WHERE `race` = @HighmountainTauren;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   0, 1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   1, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   2, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   3, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   4, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   5, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   6, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 0, 1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 1, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 2, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 3, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 4, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 5, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 6, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 7, 8, 0);

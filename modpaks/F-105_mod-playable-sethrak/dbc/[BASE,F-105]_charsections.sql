-- charsections: 22 inserts, 0 updates, 0 deletes
-- From the skin colours (option 0) of CoA's appearance catalog EsteriaSethrak.bin, flagged for character creation (17, faces 1)

-- New entries
DELETE FROM `charsections` WHERE `race` = @Sethrak;
SET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Skin,       'custom\\sethrak\\equipment\\skin-male-0.blp', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Skin,       'custom\\sethrak\\equipment\\skin-male-1.blp', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Skin,       'custom\\sethrak\\equipment\\skin-male-2.blp', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Skin,       'custom\\sethrak\\equipment\\skin-male-3.blp', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Skin,       'custom\\sethrak\\equipment\\skin-male-4.blp', '', '', 17, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Face,       '', '', '', 1, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Face,       '', '', '', 1, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Face,       '', '', '', 1, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Face,       '', '', '', 1, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Underwear,  '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Underwear,  '', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Underwear,  '', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Underwear,  '', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Male,  @Underwear,  '', '', '', 17, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Female, @Skin,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Female, @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Female, @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Female, @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Sethrak, @Female, @Underwear,  '', '', '', 17, 0, 0);

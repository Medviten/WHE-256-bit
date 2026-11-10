-- charsections: 28 inserts, 0 updates, 0 deletes
-- From the skin colours (option 0) of CoA's appearance catalog EsteriaSaberon.bin, flagged for character creation (17, faces 1)

-- New entries
DELETE FROM `charsections` WHERE `race` = @Saberon;
SET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Skin,       'custom\\saberon\\native\\textures\\982811.blp', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Skin,       'custom\\saberon\\native\\textures\\982810.blp', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Skin,       'custom\\saberon\\native\\textures\\982813.blp', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Skin,       'custom\\saberon\\native\\textures\\982812.blp', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Face,       '', '', '', 1, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Face,       '', '', '', 1, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Face,       '', '', '', 1, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Underwear,  '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Underwear,  '', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Underwear,  '', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Male,  @Underwear,  '', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Skin,       'custom\\saberon\\native\\textures\\982811.blp', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Skin,       'custom\\saberon\\native\\textures\\982810.blp', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Skin,       'custom\\saberon\\native\\textures\\982813.blp', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Skin,       'custom\\saberon\\native\\textures\\982812.blp', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Face,       '', '', '', 1, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Face,       '', '', '', 1, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Face,       '', '', '', 1, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Underwear,  '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Underwear,  '', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Underwear,  '', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Saberon, @Female, @Underwear,  '', '', '', 17, 0, 3);

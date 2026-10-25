-- charsections: 19 inserts, 0 updates, 0 deletes
-- From the skin colours (option 0) of CoA's appearance catalog EsteriaKyrian.bin, flagged for character creation (17, faces 1)

-- New entries
DELETE FROM `charsections` WHERE `race` = @Kyrian;
SET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Skin,       'custom\\kyrian\\native\\textures\\3034031.blp', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Skin,       'custom\\kyrian\\native\\textures\\3034032.blp', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Skin,       'custom\\kyrian\\native\\palettes\\male-gold-body.blp', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Face,       '', '', '', 1, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Face,       '', '', '', 1, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Underwear,  '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Underwear,  '', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Male,  @Underwear,  '', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @Skin,       'custom\\kyrian\\native\\textures\\2976405.blp', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @Skin,       'custom\\kyrian\\native\\textures\\2976406.blp', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @Face,       '', '', '', 1, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @Underwear,  '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Kyrian, @Female, @Underwear,  '', '', '', 17, 0, 1);

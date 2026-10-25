-- charsections: 37 inserts, 0 updates, 0 deletes
-- From the skin textures shipped with the model (WallCraft has no rows for it), flagged for character creation (17, faces 1)

-- New entries
DELETE FROM `charsections` WHERE `race` = @Centaur;
SET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);
INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Skin,       'Character\\Centaur\\Male\\CentaurSkin.blp', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Skin,       'Character\\Centaur\\Male\\CentaurSkinBlack.blp', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Skin,       'Character\\Centaur\\Male\\CentaurSkinDarkgray.blp', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Skin,       'Character\\Centaur\\Male\\CentaurSkinGray.blp', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Skin,       'Character\\Centaur\\Male\\CentaurSkinWhite.blp', '', '', 17, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Skin,       'Character\\Centaur\\Male\\CentaurSkinYellow.blp', '', '', 17, 0, 5),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Face,       '', '', '', 1, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Face,       '', '', '', 1, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Face,       '', '', '', 1, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Face,       '', '', '', 1, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Face,       '', '', '', 1, 0, 5),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Underwear,  '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Underwear,  '', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Underwear,  '', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Underwear,  '', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Underwear,  '', '', '', 17, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Male,  @Underwear,  '', '', '', 17, 0, 5),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Skin,       'Character\\Centaur\\Female\\CentaurCasterSkinBrown.blp', 'Character\\Centaur\\Female\\CentaurCasterSkinBrown_Alpha.blp', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Skin,       'Character\\Centaur\\Female\\CentaurCasterSkinBlack.blp', 'Character\\Centaur\\Female\\CentaurCasterSkinBlack_Alpha.blp', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Skin,       'Character\\Centaur\\Female\\CentaurCasterSkinGray.blp', 'Character\\Centaur\\Female\\CentaurCasterSkinGray_Alpha.blp', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Skin,       'Character\\Centaur\\Female\\CentaurCasterSkinWhite.blp', 'Character\\Centaur\\Female\\CentaurCasterSkinWhite_Alpha.blp', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Skin,       'Character\\Centaur\\Female\\CentaurCasterSkinYellow.blp', 'Character\\Centaur\\Female\\CentaurCasterSkinYellow_Alpha.blp', '', 17, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Face,       '', '', '', 1, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Face,       '', '', '', 1, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Face,       '', '', '', 1, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Face,       '', '', '', 1, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Face,       '', '', '', 1, 0, 4),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @FacialHair, '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Hair,       '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Underwear,  '', '', '', 17, 0, 0),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Underwear,  '', '', '', 17, 0, 1),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Underwear,  '', '', '', 17, 0, 2),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Underwear,  '', '', '', 17, 0, 3),
(@CharSectionsID := @CharSectionsID +1, @Centaur, @Female, @Underwear,  '', '', '', 17, 0, 4);

-- creaturedisplayinfo: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @WorgenMaleDisplay,    @WorgenFemaleDisplay, 
    @LordHarfordDisplay,   @GallyLumpstainDisplay,
    @MountainHorseDisplay, @SwiftMountainHorseDisplay
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@WorgenMaleDisplay,         @WorgenMaleModel,   0, @WorgenMaleDisplayExtra,     '1.0000000000000000', 255, '',               '', '', '', 3, 0, 0, 0, 0, 0),
(@WorgenFemaleDisplay,       @WorgenFemaleModel, 0, @WorgenFemaleDisplayExtra,   '1.0000000000000000', 255, '',               '', '', '', 3, 0, 0, 0, 0, 0),
(@LordHarfordDisplay,        @WorgenMaleModel,   0, @LordHarfordDisplayExtra,    '1.0000000000000000', 255, '',               '', '', '', 3, 0, 0, 0, 0, 0),
(@GallyLumpstainDisplay,     @GoblinMaleModel,   0, @GallyLumpstainDisplayExtra, '1.0000000000000000', 255, '',               '', '', '', 1, 0, 0, 0, 0, 0),
(@MountainHorseDisplay,      @HorseModel,        0,                         0,   '1.0000000000000000', 255, 'HorseSkinBlack', '', '', '', 1, 0, 0, 0, 0, 0), -- black mountain horse
(@SwiftMountainHorseDisplay, @HorseModel,        0,                         0,   '1.0000000000000000', 255, 'HorseSkinBrown', '', '', '', 1, 0, 0, 0, 0, 0); -- brown mountain horse

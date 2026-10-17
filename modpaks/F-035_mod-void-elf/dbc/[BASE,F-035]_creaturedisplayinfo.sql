-- creaturedisplayinfo: 3 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @VoidElfMaleDisplay,    @VoidElfFemaleDisplay, 
    @VoidElfMount1Display
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@VoidElfMaleDisplay,   @VoidElfMaleModel,   0, @VoidElfMaleDisplayExtra,     '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0),
(@VoidElfFemaleDisplay, @VoidElfFemaleModel, 0, @VoidElfFemaleDisplayExtra,   '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0),
(@VoidElfMount1Display,  @VoidElfMount1Model,  0,                          0,   '1.0000000000000000', 255, '', '', '', '', 1, 0, 0, 0, 0, 0);

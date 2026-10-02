-- creaturedisplayinfo: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @GilneanMaleDisplay,   @GilneanFemaleDisplay
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@GilneanMaleDisplay,        @GilneanMaleModel,   0, @GilneanMaleDisplayExtra,                      1, 255, '',               '', '', '', 1, 0, 0, 0, 0, 0),
(@GilneanFemaleDisplay,      @GilneanFemaleModel, 0, @GilneanFemaleDisplayExtra,                    1, 255, '',               '', '', '', 1, 0, 0, 0, 0, 0);

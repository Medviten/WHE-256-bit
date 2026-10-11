-- creaturedisplayinfo: 3 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @NightborneMaleDisplay,   @NightborneFemaleDisplay,
    @NightborneManasaber
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@NightborneMaleDisplay,   @NightborneMaleModel,   0, @NightborneMaleDisplayExtra,   '1', 255, '',                   '',                      '', '', 3, 0, 0, 0, 0, 0),
(@NightborneFemaleDisplay, @NightborneFemaleModel, 0, @NightborneFemaleDisplayExtra, '1', 255, '',                   '',                      '', '', 3, 0, 0, 0, 0, 0),
(@NightborneManasaber, @CaravanHyena2Model, 0,                          0,   1, 255, '', '', '', '', 1, 0, 0, 0, 0, 0);

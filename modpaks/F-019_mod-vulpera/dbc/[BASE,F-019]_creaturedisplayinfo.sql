-- creaturedisplayinfo: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @VulperaMaleDisplay,   @VulperaFemaleDisplay,
    @CaravanHyena1Display, @CaravanHyena2Display
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@VulperaMaleDisplay,   @VulperaMaleModel,   0, @VulperaMaleDisplayExtra,   '1', 255, '',                   '',                      '', '', 3, 0, 0, 0, 0, 0),
(@VulperaFemaleDisplay, @VulperaFemaleModel, 0, @VulperaFemaleDisplayExtra, '1', 255, '',                   '',                      '', '', 3, 0, 0, 0, 0, 0),
(@CaravanHyena1Display, @CaravanHyena1Model, 0,                          0,   1, 255, 'vulperamount_tan', 'vulperamount_saddle', '', '', 1, 0, 0, 0, 0, 0),
(@CaravanHyena2Display, @CaravanHyena2Model, 0,                          0,   1, 255, 'vulperamount2_tan', 'vulperamount2_saddle', '', '', 1, 0, 0, 0, 0, 0);

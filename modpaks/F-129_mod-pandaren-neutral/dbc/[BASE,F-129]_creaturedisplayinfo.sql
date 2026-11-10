-- creaturedisplayinfo: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @NeutralPandarenMaleDisplay, @NeutralPandarenFemaleDisplay,
    @NeutralPandarenMount1Display, @NeutralPandarenMount2Display, @NeutralPandarenMount3Display, @NeutralPandarenMount4Display
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@NeutralPandarenMaleDisplay,   @PandarenMaleModel,   0, @NeutralPandarenMaleDisplayExtra,   '1.0000000000000000', 255, '',                         '',                              '', '', 3, 0, 0, 0, 0, 0),
(@NeutralPandarenFemaleDisplay, @PandarenFemaleModel, 0, @NeutralPandarenFemaleDisplayExtra, '1.0000000000000000', 255, '',                         '',                              '', '', 3, 0, 0, 0, 0, 0),
(@NeutralPandarenMount1Display, @NeutralPandarenMount1Model,   0,                                   0,                    2, 255, 'ridingdragonturtleblue',   'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0),
(@NeutralPandarenMount2Display, @NeutralPandarenMount2Model,   0,                                   0,                    2, 255, 'ridingdragonturtlepurple', 'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0),
(@NeutralPandarenMount3Display, @NeutralPandarenMount3Model,   0,                                   0,                    2, 255, 'ridingdragonturtlegreen',  'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0),
(@NeutralPandarenMount4Display, @NeutralPandarenMount4Model,   0,                                   0,                    2, 255, 'ridingdragonturtleblack',  'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0);

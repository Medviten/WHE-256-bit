-- creaturedisplayinfo: 2 inserts, 0 updates, 0 deletes

-- New entries (display scale as CoA's displays 977475/977476)
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (@FurbolgMaleDisplay, @FurbolgFemaleDisplay);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@FurbolgMaleDisplay,   @FurbolgMaleModel, 0, @FurbolgMaleDisplayExtra,   '1.3500000238000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0),
(@FurbolgFemaleDisplay, @FurbolgFemaleModel, 0, @FurbolgFemaleDisplayExtra, '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0);

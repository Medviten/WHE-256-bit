-- creaturedisplayinfo: 2 inserts, 0 updates, 0 deletes

-- New entries (display scale as CoA's displays 977750/977751)
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (@MoguMaleDisplay, @MoguFemaleDisplay);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@MoguMaleDisplay,   @MoguMaleModel, 0, @MoguMaleDisplayExtra,   '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0),
(@MoguFemaleDisplay, @MoguFemaleModel, 0, @MoguFemaleDisplayExtra, '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0);

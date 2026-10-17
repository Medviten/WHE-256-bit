-- creaturedisplayinfo: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @LightforgedDraeneiMaleDisplay, @LightforgedDraeneiFemaleDisplay,
    @LightforgedDraeneiMount1Display, @LightforgedDraeneiMount2Display, @LightforgedDraeneiMount3Display, @LightforgedDraeneiMount4Display
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@LightforgedDraeneiMaleDisplay,   @LightforgedDraeneiMaleModel,   0, @LightforgedDraeneiMaleDisplayExtra,   '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0),
(@LightforgedDraeneiFemaleDisplay, @LightforgedDraeneiFemaleModel, 0, @LightforgedDraeneiFemaleDisplayExtra, '1.0000000000000000', 255, '', '', '', '', 3, 0, 0, 0, 0, 0),
(@LightforgedDraeneiMount1Display, @LightforgedDraeneiMount1Model, 0, 0, '1.0000000000000000', 255, 'lightforgedelekk_darklight', '', '', '', 1, 0, 0, 0, 0, 0),
(@LightforgedDraeneiMount2Display, @LightforgedDraeneiMount2Model, 0, 0, '1.0000000000000000', 255, 'lightforgedelekk_amethyst',  '', '', '', 1, 0, 0, 0, 0, 0),
(@LightforgedDraeneiMount3Display, @LightforgedDraeneiMount3Model, 0, 0, '1.0000000000000000', 255, 'lightforgedelekk_blue',      '', '', '', 1, 0, 0, 0, 0, 0),
(@LightforgedDraeneiMount4Display, @LightforgedDraeneiMount4Model, 0, 0, '1.0000000000000000', 255, 'lightforgedelekk_holy',      '', '', '', 1, 0, 0, 0, 0, 0);

-- itemdisplayinfo: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `itemdisplayinfo` WHERE `id` IN (
    @LightforgedDraeneiMount1ItemDisplay, @LightforgedDraeneiMount2ItemDisplay,
    @LightforgedDraeneiMount3ItemDisplay, @LightforgedDraeneiMount4ItemDisplay
);
INSERT INTO `itemdisplayinfo` (`id`, `left_model`, `right_model`, `left_model_texture`, `right_model_texture`, `icon_1`, `icon_2`, `geoset_group_1`, `geoset_group_2`, `geoset_group_3`, `flags`, `spell_visual_id`, `group_sound_index`, `helmet_geoset_male`, `helmet_geoset_female`, `upper_arm_texture`, `lower_arm_texture`, `hands_texture`, `upper_torso_texture`, `lower_torso_texture`, `upper_leg_texture`, `lower_leg_texture`, `foot_texture`, `item_visual`, `particle_colour_id`) VALUES
(@LightforgedDraeneiMount1ItemDisplay, '', '', '', '', @LightforgedDraeneiMount1IconName, '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0),
(@LightforgedDraeneiMount2ItemDisplay, '', '', '', '', @LightforgedDraeneiMount2IconName, '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0),
(@LightforgedDraeneiMount3ItemDisplay, '', '', '', '', @LightforgedDraeneiMount3IconName, '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0),
(@LightforgedDraeneiMount4ItemDisplay, '', '', '', '', @LightforgedDraeneiMount4IconName, '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0);

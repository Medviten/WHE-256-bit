-- itemdisplayinfo: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `itemdisplayinfo` WHERE `id` IN (
    @HordePandarenMount1ItemDisplay, @HordePandarenMount2ItemDisplay, @HordePandarenMount3ItemDisplay, @HordePandarenMount4ItemDisplay
);
INSERT INTO `itemdisplayinfo` (`id`, `left_model`, `right_model`, `left_model_texture`, `right_model_texture`, `icon_1`, `icon_2`, `geoset_group_1`, `geoset_group_2`, `geoset_group_3`, `flags`, `spell_visual_id`, `group_sound_index`, `helmet_geoset_male`, `helmet_geoset_female`, `upper_arm_texture`, `lower_arm_texture`, `hands_texture`, `upper_torso_texture`, `lower_torso_texture`, `upper_leg_texture`, `lower_leg_texture`, `foot_texture`, `item_visual`, `particle_colour_id`) VALUES
(@HordePandarenMount1ItemDisplay,   '', '', '', '', 'ability_mount_pandaranmountblue',   '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0),
(@HordePandarenMount2ItemDisplay, '', '', '', '', 'ability_mount_pandaranmountpurple', '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0),
(@HordePandarenMount3ItemDisplay,  '', '', '', '', 'ability_mount_pandaranmountgreen',  '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0),
(@HordePandarenMount4ItemDisplay,  '', '', '', '', 'ability_mount_pandaranmountblack',  '', 0, 0, 0, 0, 0, 16, 0, 0, '', '', '', '', '', '', '', '', 0, 0);

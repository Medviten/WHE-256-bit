-- creaturedisplayinfo: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (
    @HordePandarenMaleDisplay, @HordePandarenFemaleDisplay,
    @DragonTurtleBlueDisplay, @DragonTurtlePurpleDisplay, @DragonTurtleGreenDisplay, @DragonTurtleBlackDisplay
);
INSERT INTO `creaturedisplayinfo` (`id`, `model_id`, `sound_id`, `extended_display_info_id`, `creature_model_scale`, `creature_model_alpha`, `texture_variation_1`, `texture_variation_2`, `texture_variation_3`, `portrait_texture_name`, `blood_level`, `blood_id`, `npc_sound_id`, `praticle_color_id`, `creature_geoset_data`, `obj_effect_package_id`) VALUES
(@HordePandarenMaleDisplay,   @PandarenMaleModel,   0, @HordePandarenMaleDisplayExtra,   '1.0000000000000000', 255, '',                         '',                              '', '', 3, 0, 0, 0, 0, 0),
(@HordePandarenFemaleDisplay, @PandarenFemaleModel, 0, @HordePandarenFemaleDisplayExtra, '1.0000000000000000', 255, '',                         '',                              '', '', 3, 0, 0, 0, 0, 0),
(@DragonTurtleBlueDisplay,    @DragonTurtleModel,   0,                                0,                    2, 255, 'ridingdragonturtleblue',   'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0),
(@DragonTurtlePurpleDisplay,  @DragonTurtleModel,   0,                                0,                    2, 255, 'ridingdragonturtlepurple', 'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0),
(@DragonTurtleGreenDisplay,   @DragonTurtleModel,   0,                                0,                    2, 255, 'ridingdragonturtlegreen',  'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0),
(@DragonTurtleBlackDisplay,   @DragonTurtleModel,   0,                                0,                    2, 255, 'ridingdragonturtleblack',  'ridingdragonturtlesaddlebrown', '', '', 1, 0, 0, 0, 0, 0);


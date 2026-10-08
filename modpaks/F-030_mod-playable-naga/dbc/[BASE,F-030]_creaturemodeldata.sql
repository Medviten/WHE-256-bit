-- creaturemodeldata: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `creaturemodeldata` WHERE `id` IN (@NagaMaleModel, @NagaFemaleModel);
INSERT INTO `creaturemodeldata` (`id`, `flags`, `model_path`, `size_class`, `model_scale`, `blood_id`, `footprint_texture_id`, `footprint_texture_length`, `footprint_texture_width`, `footprint_particle_scale`, `foley_material_id`, `footstep_shake_size`, `death_thud_shake_size`, `sound_data`, `collision_width`, `collision_height`, `mount_height`, `geo_box_min_x`, `geo_box_min_y`, `geo_box_min_z`, `geo_box_max_x`, `geo_box_max_y`, `geo_box_max_z`, `world_effect_scale`, `attached_effect_scale`, `missile_collision_radius`, `missile_collision_push`, `missile_collision_raise`) VALUES
(@NagaMaleModel,   2052, @NagaMaleModelPath,   1, 1, 1, 1, 12, 10, 1, 0, 0, 0, 2281, 0.6111, 2.031, 1.036183, -0.576729, -0.544345, -0.000694, 0.368137, 0.535902,   2.1292, 1, 1, 0, 0, 0),
(@NagaFemaleModel, 2052, @NagaFemaleModelPath, 1, 1, 1, 1, 12, 10, 1, 0, 0, 0, 2282, 0.4167, 1.913, 1.002637, -0.487307, -0.359981, -0.002223, 0.275955, 0.370421, 1.924935, 1, 1, 0, 0, 0);

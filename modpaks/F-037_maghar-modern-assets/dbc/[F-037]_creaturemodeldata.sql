-- creaturemodeldata: 2 inserts, 0 updates, 0 deletes
-- Copies of the stock orc models (51, 52) with the modern model paths

-- New entries
DELETE FROM `creaturemodeldata` WHERE `id` IN (@MagharOrcModernMaleModel, @MagharOrcModernFemaleModel);
INSERT INTO `creaturemodeldata` (`id`, `flags`, `model_path`, `size_class`, `model_scale`, `blood_id`, `footprint_texture_id`, `footprint_texture_length`, `footprint_texture_width`, `footprint_particle_scale`, `foley_material_id`, `footstep_shake_size`, `death_thud_shake_size`, `sound_data`, `collision_width`, `collision_height`, `mount_height`, `geo_box_min_x`, `geo_box_min_y`, `geo_box_min_z`, `geo_box_max_x`, `geo_box_max_y`, `geo_box_max_z`, `world_effect_scale`, `attached_effect_scale`, `missile_collision_radius`, `missile_collision_push`, `missile_collision_raise`)
SELECT @MagharOrcModernMaleModel, `flags`, @MagharOrcModernMaleModelPath, `size_class`, `model_scale`, `blood_id`, `footprint_texture_id`, `footprint_texture_length`, `footprint_texture_width`, `footprint_particle_scale`, `foley_material_id`, `footstep_shake_size`, `death_thud_shake_size`, `sound_data`, `collision_width`, `collision_height`, `mount_height`, `geo_box_min_x`, `geo_box_min_y`, `geo_box_min_z`, `geo_box_max_x`, `geo_box_max_y`, `geo_box_max_z`, `world_effect_scale`, `attached_effect_scale`, `missile_collision_radius`, `missile_collision_push`, `missile_collision_raise`
FROM `creaturemodeldata` WHERE `id` = @MagharOrcMaleModel
UNION ALL
SELECT @MagharOrcModernFemaleModel, `flags`, @MagharOrcModernFemaleModelPath, `size_class`, `model_scale`, `blood_id`, `footprint_texture_id`, `footprint_texture_length`, `footprint_texture_width`, `footprint_particle_scale`, `foley_material_id`, `footstep_shake_size`, `death_thud_shake_size`, `sound_data`, `collision_width`, `collision_height`, `mount_height`, `geo_box_min_x`, `geo_box_min_y`, `geo_box_min_z`, `geo_box_max_x`, `geo_box_max_y`, `geo_box_max_z`, `world_effect_scale`, `attached_effect_scale`, `missile_collision_radius`, `missile_collision_push`, `missile_collision_raise`
FROM `creaturemodeldata` WHERE `id` = @MagharOrcFemaleModel;

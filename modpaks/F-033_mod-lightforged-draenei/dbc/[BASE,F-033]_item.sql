-- item: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @LightforgedFelcrusherHolyItem, @LightforgedFelcrusherPurpleItem,
    @LightforgedFelcrusherBlueItem, @LightforgedFelcrusherDarkItem
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@LightforgedFelcrusherHolyItem,   15, 5, -1,  4, 132261,  0, 0),
(@LightforgedFelcrusherPurpleItem, 15, 5, -1,  4, 132261,  0, 0),
(@LightforgedFelcrusherBlueItem,   15, 5, -1,  4, 132261,  0, 0),
(@LightforgedFelcrusherDarkItem,   15, 5, -1,  4, 132261,  0, 0);

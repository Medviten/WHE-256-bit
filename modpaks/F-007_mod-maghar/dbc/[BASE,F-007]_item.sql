-- item: 1 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (@MagharOrcMount1Item);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@MagharOrcMount1Item,   15, 5, -1,  4, @MagharOrcMount1ItemDisplay,  0, 0);

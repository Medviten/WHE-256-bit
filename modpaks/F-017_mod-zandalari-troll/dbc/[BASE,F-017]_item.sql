-- item: 1 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (@ZandalariTrollMount1Item);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@ZandalariTrollMount1Item,   15, 5, -1,  4, @ZandalariTrollMount1ItemDisplay,  0, 0);

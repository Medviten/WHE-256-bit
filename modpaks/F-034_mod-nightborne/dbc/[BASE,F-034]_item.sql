-- item: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (@NightborneMount1Item);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@NightborneMount1Item, 15, 5, -1,  4, @NightborneMount1ItemDisplay,  0, 0);

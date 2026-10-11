-- item: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (@NightborneManasaberItem);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@NightborneManasaberItem, 15, 5, -1,  4, @NightborneManasaberItemDisplay,  0, 0);

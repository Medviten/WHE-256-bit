-- item: 1 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` = @HighmountainThunderhoofItem;
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@HighmountainThunderhoofItem, 15, 5, -1,  4, @HighmountainThunderhoofItemDisplay,  0, 0);

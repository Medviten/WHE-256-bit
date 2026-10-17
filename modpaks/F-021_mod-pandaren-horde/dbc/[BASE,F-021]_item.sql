-- item: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @HordePandarenMount1Item, @HordePandarenMount2Item, @HordePandarenMount3Item, @HordePandarenMount4Item
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@HordePandarenMount1Item,   15, 5, -1,  4, @HordePandarenMount1ItemDisplay,    0, 0),
(@HordePandarenMount2Item, 15, 5, -1,  4, @HordePandarenMount2ItemDisplay,  0, 0),
(@HordePandarenMount3Item,  15, 5, -1,  4, @HordePandarenMount3ItemDisplay,   0, 0),
(@HordePandarenMount4Item,  15, 5, -1,  4, @HordePandarenMount4ItemDisplay,   0, 0);

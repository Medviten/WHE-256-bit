-- item: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @VulperaMount1Item, @VulperaMount2Item
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@VulperaMount1Item, 15, 5, -1,  4, @VulperaMount1ItemDisplay,  0, 0),
(@VulperaMount2Item, 15, 5, -1,  4, @VulperaMount2ItemDisplay,  0, 0);

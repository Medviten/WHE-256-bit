-- item: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @AlliancePandarenMount1Item, @AlliancePandarenMount2Item, @AlliancePandarenMount3Item, @AlliancePandarenMount4Item
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@AlliancePandarenMount1Item,   15, 5, -1,  4, @AlliancePandarenMount1ItemDisplay,    0, 0),
(@AlliancePandarenMount2Item, 15, 5, -1,  4, @AlliancePandarenMount2ItemDisplay,  0, 0),
(@AlliancePandarenMount3Item,  15, 5, -1,  4, @AlliancePandarenMount3ItemDisplay,   0, 0),
(@AlliancePandarenMount4Item,  15, 5, -1,  4, @AlliancePandarenMount4ItemDisplay,   0, 0);

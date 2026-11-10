-- item: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @NeutralPandarenMount1Item, @NeutralPandarenMount2Item, @NeutralPandarenMount3Item, @NeutralPandarenMount4Item
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@NeutralPandarenMount1Item,   15, 5, -1,  4, @NeutralPandarenMount1ItemDisplay,    0, 0),
(@NeutralPandarenMount2Item, 15, 5, -1,  4, @NeutralPandarenMount2ItemDisplay,  0, 0),
(@NeutralPandarenMount3Item,  15, 5, -1,  4, @NeutralPandarenMount3ItemDisplay,   0, 0),
(@NeutralPandarenMount4Item,  15, 5, -1,  4, @NeutralPandarenMount4ItemDisplay,   0, 0);

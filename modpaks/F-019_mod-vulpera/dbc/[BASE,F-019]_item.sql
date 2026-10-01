-- item: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @CaravanHyena1Item, @CaravanHyena2Item
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@CaravanHyena1Item, 15, 5, -1,  4, @CaravanHyena1ItemDisplay,  0, 0),
(@CaravanHyena2Item, 15, 5, -1,  4, @CaravanHyena2ItemDisplay,  0, 0);

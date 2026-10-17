-- item: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @LightforgedDraeneiMount1Item, @LightforgedDraeneiMount2Item,
    @LightforgedDraeneiMount3Item, @LightforgedDraeneiMount4Item
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@LightforgedDraeneiMount1Item, 15, 5, -1,  4, @LightforgedDraeneiMount1ItemDisplay,  0, 0),
(@LightforgedDraeneiMount2Item, 15, 5, -1,  4, @LightforgedDraeneiMount2ItemDisplay,  0, 0),
(@LightforgedDraeneiMount3Item, 15, 5, -1,  4, @LightforgedDraeneiMount3ItemDisplay,  0, 0),
(@LightforgedDraeneiMount4Item, 15, 5, -1,  4, @LightforgedDraeneiMount4ItemDisplay,  0, 0);

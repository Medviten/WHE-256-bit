-- item: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @DragonTurtleBlueItem, @DragonTurtlePurpleItem, @DragonTurtleGreenItem, @DragonTurtleBlackItem
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@DragonTurtleBlueItem,   15, 5, -1,  4, @DragonTurtleBlueItemDisplay,    0, 0),
(@DragonTurtlePurpleItem, 15, 5, -1,  4, @DragonTurtlePurpleItemDisplay,  0, 0),
(@DragonTurtleGreenItem,  15, 5, -1,  4, @DragonTurtleGreenItemDisplay,   0, 0),
(@DragonTurtleBlackItem,  15, 5, -1,  4, @DragonTurtleBlackItemDisplay,   0, 0);

-- I-384: Item.dbc rows of the three Taming Rods and the Attuned Orb of Dominion
DELETE FROM `item` WHERE `id` BETWEEN 84606 AND 84609;
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(84606, 12, 0, -1, -1, 26595, 0, 0),
(84607, 12, 0, -1, -1, 26595, 0, 0),
(84608, 12, 0, -1, -1, 26595, 0, 0),
(84609, 12, 0, -1, 3, 39424, 0, 0);

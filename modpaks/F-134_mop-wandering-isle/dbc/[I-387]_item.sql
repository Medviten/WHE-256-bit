-- I-387: Item.dbc rows of the three Taming Rods and the Attuned Orb of Dominion
DELETE FROM `item` WHERE `id` BETWEEN 84610 AND 84613;
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(84610, 12, 0, -1, -1, 26595, 0, 0),
(84611, 12, 0, -1, -1, 26595, 0, 0),
(84612, 12, 0, -1, -1, 26595, 0, 0),
(84613, 12, 0, -1, 3, 39424, 0, 0);

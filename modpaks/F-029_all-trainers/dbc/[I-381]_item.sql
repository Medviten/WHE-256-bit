-- I-381 F-029 hunter taming: Item.dbc rows of the six Taming Rods
DELETE FROM `item` WHERE `id` BETWEEN 84600 AND 84605;
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(84600, 12, 0, -1, -1, 26595, 0, 0),
(84601, 12, 0, -1, -1, 26595, 0, 0),
(84602, 12, 0, -1, -1, 26595, 0, 0),
(84603, 12, 0, -1, -1, 26595, 0, 0),
(84604, 12, 0, -1, -1, 26595, 0, 0),
(84605, 12, 0, -1, -1, 26595, 0, 0);

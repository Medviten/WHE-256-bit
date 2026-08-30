/* Add models for racial mounts and goblin racial bank NPC */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (36613, 46754, 46755, 55272, 55273, 55274, 55275, 55276, 55277);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
	(36613, 0, 32385, 1, 1, 12340), -- Gobber
	(46754, 0, 35249, 1, 1, 12340), -- Goblin Trike
	(46755, 0, 35250, 1, 1, 12340), -- Goblin Turbo-Trike
    (55272, 0, 39096, 1, 1, 12340), -- Mountain Horse
	(55273, 0, 39095, 1, 1, 12340), -- Swift Mountain Horse
	(55274, 0, 94133, 1, 1, 12340), -- Running Wild Male
	(55275, 0, 94134, 1, 1, 12340), -- Running Wild Female
	(55276, 0, 94135, 1, 1, 12340), -- Gilnean Male
	(55277, 0, 94136, 1, 1, 12340); -- Gilnean Female

-- Removing 'An Injured Colleage' (13986) from questgiver, no longer valid quest as questender 'Aponi Brightmane' (34526 --> 142011) has been updated
DELETE FROM `creature_queststarter` WHERE quest = 13986
-- INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
-- (35471, 13986);

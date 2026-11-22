-- .tele targets for Open Azeroth's Cataclysm zones (positions from OA's GM teleports).
-- Stock's "Gilneas" (1473, outside the old wall) is replaced by OA's Gilneas City. Kezan is the goblin start at KTC
-- headquarters (F-013's @GoblinStart): OA's own spot, moved 533.333 east as F-013 moves Kezan, lay 4.4 yards under the
-- ground. GilneasCity is Gilneas again: its own chunks lie under its canals' water. Stock's "EasternPlaguelands"
-- (319) lies over a gap in OA's Cataclysm terrain: it is Light's Hope Chapel now, by its flight master. Deepholm and the Maelstrom need dbc/[F-010]_map.sql's expansion 2.
-- No Stonecore (725): it's a dungeon with no server map files or instance_template row.
DELETE FROM `game_tele` WHERE `id` BETWEEN 86000 AND 86016 OR `name` IN ('TolBarad', 'Surwich', 'Gilneas',
    'CavernsOfConsumption', 'Vashj''ir', 'Vashjir', 'LostIsles', 'Maelstrom', 'TheMaelstrom', 'Kezan', 'Crestfall',
    'Havenswood', 'Deepholm', 'EasternPlaguelands', 'GilneasCity');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES
(86000, -1114.662964, 7041.917480, 94.632301, 0.067694, 0, 'TolBarad'),
(86001, -12708.246094, -2868.473389, 1.392930, 0.374838, 0, 'Surwich'),
(86002, -1748.287720, 1370.000854, 19.935007, 3.954281, 0, 'Gilneas'),
(86003, 8906.926758, -3991.429932, 160.995148, 3.280236, 1, 'CavernsOfConsumption'),
(86004, -5505.588379, 3811.846924, 1.693684, 0.592196, 0, 'Vashj''ir'),
(86005, -5505.588379, 3811.846924, 1.693684, 0.592196, 0, 'Vashjir'),
(86006, 144.075729, -10833.707031, 88.233757, 2.928636, 1, 'LostIsles'),
(86007, 822.653748, 1095.179321, 49.360321, 4.855340, 1469, 'Maelstrom'),
(86008, 822.653748, 1095.179321, 49.360321, 4.855340, 1469, 'TheMaelstrom'),
(86009, -8956.5, -11429.5, 104.82, 4.562, 1, 'Kezan'),
(86010, -5483.664551, 10405.538086, 55.779266, 0.053367, 0, 'Crestfall'),
(86011, 1729.306763, 5524.595215, 59.227848, 2.632434, 0, 'Havenswood'),
(86014, 988.000000, 520.000000, -49.334774, 0.200274, 646, 'Deepholm'),
(86015, 2322.0, -5293.0, 82.5, 0.341, 0, 'EasternPlaguelands'),
(86016, -1748.287720, 1370.000854, 19.935007, 3.954281, 0, 'GilneasCity');

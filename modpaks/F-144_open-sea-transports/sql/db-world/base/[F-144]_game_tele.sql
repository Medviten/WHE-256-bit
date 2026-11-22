-- .tele targets for F-144's transport stops, each by an NPC who stands there (stock's creature spawns):
--   AuberdineDock: The Bravery's pier, by a sentinel (guid 38987). Stock's "Auberdine" is the town
--   StormwindDock: The Bravery's pier in Stormwind Harbor, by Nayura <Dockmaster> (guid 49592). Stock's
--                  "StormwindHarbor" is the harbour's entrance
--   OrgrimmarZeppelin, UndercityZeppelin: The Thundercaller's berths, by Frezza (guid 3464) and Zapetta (guid 32036).
--                  Stock's "DurotarZeppelin" and "TirisfalGladesZeppelin" reach the same towers under other names
DELETE FROM `game_tele` WHERE `id` BETWEEN 14400 AND 14403 OR `name` IN ('AuberdineDock', 'StormwindDock',
    'OrgrimmarZeppelin', 'UndercityZeppelin');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES
(14400, 6430.0, 819.0, 6.1, 2.95, 1, 'AuberdineDock'),
(14401, -8643.0, 1327.0, 5.8, 1.82, 0, 'StormwindDock'),
(14402, 1333.0, -4646.0, 54.1, 5.03, 1, 'OrgrimmarZeppelin'),
(14403, 2063.0, 284.0, 97.6, 5.31, 0, 'UndercityZeppelin');

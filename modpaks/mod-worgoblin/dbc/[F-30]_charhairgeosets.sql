-- [F-30] mod-worgoblin: charhairgeosets
-- Reintroduces Fel Orc entries as race 34.

DELETE FROM `charhairgeosets` WHERE `id` = 264;
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES (264, 34, 0, 0, 2, 0);
DELETE FROM `charhairgeosets` WHERE `id` = 265;
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES (265, 34, 1, 0, 2, 0);

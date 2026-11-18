-- I-387: spell focus of the Wandering Isle summoning circle (gameobject 901040), as [I-375]'s 1651
DELETE FROM `spellfocusobject` WHERE id = 1653;
INSERT INTO `spellfocusobject` SET
  id = 1653,
  name_enus = 'Wandering Isle Summoning Circle',
  name_flags = 16712190;

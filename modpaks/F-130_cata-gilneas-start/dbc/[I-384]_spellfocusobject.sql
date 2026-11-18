-- I-384: spell focus of Vitus Darkwalker's summoning circle (gameobject 901020), as [I-375]'s 1651 on the Lost Isles
DELETE FROM `spellfocusobject` WHERE id = 1652;
INSERT INTO `spellfocusobject` SET
  id = 1652,
  name_enus = 'Gilneas Summoning Circle',
  name_flags = 16712190;

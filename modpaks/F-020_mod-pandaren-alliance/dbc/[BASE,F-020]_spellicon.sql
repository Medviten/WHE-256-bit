-- spellicon: 9 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconDragonTurtleBlue, @IconDragonTurtlePurple, @IconDragonTurtleGreen, @IconDragonTurtleBlack,
    @IconBouncy, @IconEpicurean, @IconGourmand, @IconInnerPeace, @IconQuakingPalm
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconDragonTurtleBlue,   'Interface\\Icons\\ability_mount_pandaranmountblue'),
(@IconDragonTurtlePurple, 'Interface\\Icons\\ability_mount_pandaranmountpurple'),
(@IconDragonTurtleGreen,  'Interface\\Icons\\ability_mount_pandaranmountgreen'),
(@IconDragonTurtleBlack,  'Interface\\Icons\\ability_mount_pandaranmountblack'),
(@IconBouncy,             'Interface\\Icons\\pandarenracial_bouncy'),
(@IconEpicurean,          'Interface\\Icons\\pandarenracial_epicurean'),
(@IconGourmand,           'Interface\\Icons\\pandarenracial_gourmand'),
(@IconInnerPeace,         'Interface\\Icons\\pandarenracial_innerpeace'),
(@IconQuakingPalm,        'Interface\\Icons\\pandarenracial_quiveringpain');

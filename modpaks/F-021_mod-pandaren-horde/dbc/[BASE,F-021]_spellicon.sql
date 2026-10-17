-- spellicon: 9 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @HordePandarenMount1IconID, @HordePandarenMount2IconID, @HordePandarenMount3IconID, @HordePandarenMount4IconID,
    @IconBouncy, @IconEpicurean, @IconGourmand, @IconInnerPeace, @IconQuakingPalm
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@HordePandarenMount1IconID,   'Interface\\Icons\\ability_mount_pandaranmountblue'),
(@HordePandarenMount2IconID, 'Interface\\Icons\\ability_mount_pandaranmountpurple'),
(@HordePandarenMount3IconID,  'Interface\\Icons\\ability_mount_pandaranmountgreen'),
(@HordePandarenMount4IconID,  'Interface\\Icons\\ability_mount_pandaranmountblack'),
(@IconBouncy,             'Interface\\Icons\\pandarenracial_bouncy'),
(@IconEpicurean,          'Interface\\Icons\\pandarenracial_epicurean'),
(@IconGourmand,           'Interface\\Icons\\pandarenracial_gourmand'),
(@IconInnerPeace,         'Interface\\Icons\\pandarenracial_innerpeace'),
(@IconQuakingPalm,        'Interface\\Icons\\pandarenracial_quiveringpain');

-- spellicon: 9 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @NeutralPandarenMount1IconID, @NeutralPandarenMount2IconID, @NeutralPandarenMount3IconID, @NeutralPandarenMount4IconID,
    @IconBouncy, @IconEpicurean, @IconGourmand, @IconInnerPeace, @IconQuakingPalm
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@NeutralPandarenMount1IconID,   'Interface\\Icons\\ability_mount_pandaranmountblue'),
(@NeutralPandarenMount2IconID, 'Interface\\Icons\\ability_mount_pandaranmountpurple'),
(@NeutralPandarenMount3IconID,  'Interface\\Icons\\ability_mount_pandaranmountgreen'),
(@NeutralPandarenMount4IconID,  'Interface\\Icons\\ability_mount_pandaranmountblack'),
(@IconBouncy,             'Interface\\Icons\\pandarenracial_bouncy'),
(@IconEpicurean,          'Interface\\Icons\\pandarenracial_epicurean'),
(@IconGourmand,           'Interface\\Icons\\pandarenracial_gourmand'),
(@IconInnerPeace,         'Interface\\Icons\\pandarenracial_innerpeace'),
(@IconQuakingPalm,        'Interface\\Icons\\pandarenracial_quiveringpain');

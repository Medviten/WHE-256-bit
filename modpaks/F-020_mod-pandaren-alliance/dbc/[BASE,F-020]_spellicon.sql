-- spellicon: 9 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @AlliancePandarenMount1IconID, @AlliancePandarenMount2IconID, @AlliancePandarenMount3IconID, @AlliancePandarenMount4IconID,
    @IconBouncy, @IconEpicurean, @IconGourmand, @IconInnerPeace, @IconQuakingPalm
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@AlliancePandarenMount1IconID,   'Interface\\Icons\\ability_mount_pandaranmountblue'),
(@AlliancePandarenMount2IconID, 'Interface\\Icons\\ability_mount_pandaranmountpurple'),
(@AlliancePandarenMount3IconID,  'Interface\\Icons\\ability_mount_pandaranmountgreen'),
(@AlliancePandarenMount4IconID,  'Interface\\Icons\\ability_mount_pandaranmountblack'),
(@IconBouncy,             'Interface\\Icons\\pandarenracial_bouncy'),
(@IconEpicurean,          'Interface\\Icons\\pandarenracial_epicurean'),
(@IconGourmand,           'Interface\\Icons\\pandarenracial_gourmand'),
(@IconInnerPeace,         'Interface\\Icons\\pandarenracial_innerpeace'),
(@IconQuakingPalm,        'Interface\\Icons\\pandarenracial_quiveringpain');

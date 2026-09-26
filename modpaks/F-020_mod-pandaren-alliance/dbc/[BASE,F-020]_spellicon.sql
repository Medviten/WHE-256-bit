-- spellicon: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconBouncy, @IconEpicurean, @IconGourmand, @IconInnerPeace, @IconQuakingPalm
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconBouncy,      'Interface\\Icons\\pandarenracial_bouncy'),
(@IconEpicurean,   'Interface\\Icons\\pandarenracial_epicurean'),
(@IconGourmand,    'Interface\\Icons\\pandarenracial_gourmand'),
(@IconInnerPeace,  'Interface\\Icons\\pandarenracial_innerpeace'),
(@IconQuakingPalm, 'Interface\\Icons\\pandarenracial_quiveringpain');

-- spellicon: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconHMMooseMount,
    @IconBullRush, @IconMountaineer, @IconPrideOfIronhorn, @IconRuggedTenacity, @IconWasteNotWantNot
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconHMMooseMount,    'Interface\\Icons\\inv_hmmoosemount'),
(@IconBullRush,        'Interface\\Icons\\ability_racial_bullrush'),
(@IconMountaineer,     'Interface\\Icons\\ability_racial_mountaineer'),
(@IconPrideOfIronhorn, 'Interface\\Icons\\ability_racial_prideofironhorn'),
(@IconRuggedTenacity,  'Interface\\Icons\\ability_racial_ruggedtenacity'),
(@IconWasteNotWantNot, 'Interface\\Icons\\ability_racial_wastenotwantnot');

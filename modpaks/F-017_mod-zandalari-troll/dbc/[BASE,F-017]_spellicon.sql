-- spellicon: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconCityOfGold, @IconEmbraceTheLoa, @IconPterrodaxSwoop, @IconRegeneratin
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconCityOfGold,     'Interface\\Icons\\ability_racial_cityofgold'),
(@IconEmbraceTheLoa,  'Interface\\Icons\\ability_racial_embracetheloa'),
(@IconPterrodaxSwoop, 'Interface\\Icons\\ability_racial_pterrordaxswoop'),
(@IconRegeneratin,    'Interface\\Icons\\ability_racial_regeneratin');

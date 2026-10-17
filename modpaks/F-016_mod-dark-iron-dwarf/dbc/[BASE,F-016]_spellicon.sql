-- spellicon: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconDungeonDelver, @IconFireblood, @IconForgedInFlames, @IconMassProduction, @IconMoleMachine
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconDungeonDelver,  'Interface\\Icons\\ability_racial_dungeondelver'),
(@IconFireblood,      'Interface\\Icons\\ability_racial_fireblood'),
(@IconForgedInFlames, 'Interface\\Icons\\ability_racial_foregedinflames'),
(@IconMassProduction, 'Interface\\Icons\\ability_racial_massproduction'),
(@IconMoleMachine,    'Interface\\Icons\\ability_racial_molemachine');

-- Racial mount
DELETE FROM `spellicon` WHERE `id` IN (@DarkIronDwarfMount1IconID);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@DarkIronDwarfMount1IconID, @DarkIronDwarfMount1IconPath);

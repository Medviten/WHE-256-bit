-- spellicon: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconLightforgedElekk, 
    @IconDemonbane, @IconForgeOfLight, @IconHolyProvidence, @IconLightsJudgement, @IconLightsReckoning
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconLightforgedElekk, 'Interface\\Icons\\inv_lightforgedelekk'),
(@IconDemonbane,        'Interface\\Icons\\ability_racial_demonbane'),
(@IconForgeOfLight,     'Interface\\Icons\\ability_racial_forgeoflight'),
(@IconHolyProvidence,   'Interface\\Icons\\ability_racial_holyresistance'),
(@IconLightsJudgement,  'Interface\\Icons\\ability_racial_orbitalstrike'),
(@IconLightsReckoning,  'Interface\\Icons\\ability_racial_finalverdict');

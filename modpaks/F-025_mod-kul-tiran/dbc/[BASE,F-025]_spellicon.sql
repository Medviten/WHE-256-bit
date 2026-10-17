-- spellicon: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconBrushItOff, @IconChildOfTheSea, @IconHaymaker, @IconJackOfAllTrades, @IconRimeOfTheAncientMariner
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconBrushItOff,              'Interface\\Icons\\ability_racial_brushitoff'),
(@IconChildOfTheSea,           'Interface\\Icons\\ability_racial_childofthesea'),
(@IconHaymaker,                'Interface\\Icons\\ability_racial_haymaker'),
(@IconJackOfAllTrades,         'Interface\\Icons\\ability_racial_jackofalltrades'),
(@IconRimeOfTheAncientMariner, 'Interface\\Icons\\ability_racial_rimeoftheancientmariner');

-- Racial mount
DELETE FROM `spellicon` WHERE `id` IN (@KulTiranMount1IconID);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@KulTiranMount1IconID, @KulTiranMount1IconPath);

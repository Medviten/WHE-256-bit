-- spellicon: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconAncestralCall, @IconOpenSkies, @IconSavageBlood, @IconSympatheticVigor
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconAncestralCall,                'Interface\\Icons\\ability_racial_ancestralcall'),
(@IconSavageBlood,                  'Interface\\Icons\\ability_racial_pureblood'),
(@IconOpenSkies,                    'Interface\\Icons\\ability_racial_openskies'),
(@IconSympatheticVigor,             'Interface\\Icons\\ability_racial_sympatheticvigor');
